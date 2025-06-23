"use client";

import { useState } from "react";
import ClaimForm, { FormData as ClaimFormData } from "@/components/claim-form";
import UploadDocumentForm from "@/components/upload-document-form";
import { Toaster, toast } from 'react-hot-toast';

// API 返回的单条数据类型
type ApiDataItem = {
  page: number;
  code: string;
  name: string;
  value: string;
};

// 数据转换函数：将 API 数组转换为表单所需的扁平对象
const transformApiDataToFormData = (apiData: ApiDataItem[]): ClaimFormData => {
  // 1. 创建一个包含所有字段的、完整的默认表单对象
  // (修正此处的字段名以匹配 FormData 接口)
  const defaultFormData: ClaimFormData = {
    insuredName: "",
    mailingAddress: "",
    insuredIdNumber: "",
    insuredBirthDate: "",      // Corrected: Was insuredDateOfBirth
    policyHolder: "",          // Corrected: Was policyholderUnit
    currentOccupation: "",
    occupationCode: "",
    policyNumber: "",
    insuranceType: "",
    claimType: [],
    incidentCause: "",
    incidentRegion: "",
    hospitalsVisited: "",
    accidentDate: "",          // Corrected: Was incidentDateTime
    accidentLocation: "",
    accidentDescription: "",   // Corrected: Was incidentDetails
    policeName: "",            // Corrected: Was policeOfficerName
    policeContact: "",         // Corrected: Was policeContactPhone
    policeUnit: "",            // Corrected: Was handlingPoliceUnit
    beneficiaryName: "",
    beneficiaryIdNumber: "",
    beneficiaryAccount: "",    // Corrected: Was paymentAccountOption
    bankAccount: "",           // Corrected: Was bankNameAndBranch
    bankAccountCode: "",       // Corrected: Was bankCode
    accountNumber: "",
    contactAddress: "",
    mobilePhone: "",
    email: "",
    landlinePhone: "",
    applicantSignatureName: "",
    applicantIdNumber: "",
    legalGuardianName: "",
    legalGuardianIdNumber: "",
    applicationDate: "",
    authInsuredName: "",
    authInsuredDob: "",
    authInsuredIdNumber: "",
    authContractEffectiveDate: "",
    authAilmentOrInjury: "",
    authConsentingPersonName: "",
    authConsentingPersonIdNumber: "",
    authLegalGuardianSignatureName: "",
    authLegalGuardianIdNumber: "",
    authDate: "",
  };
  
  // 2. 将 API 返回的数组数据转换为一个部分对象
  const updates: Partial<ClaimFormData> = {};
  apiData.forEach(item => {
    const key = item.code as keyof ClaimFormData;
    if (key === 'claimType' && typeof item.value === 'string') {
        updates[key] = item.value.split(',').map(s => s.trim()).filter(Boolean);
    } else if (item.code in defaultFormData) { // 确保只合并接口中存在的字段
        updates[key] = item.value as any;
    }
  });

  // 3. 将 API 数据合并到默认对象上，返回一个完整的对象
  return { ...defaultFormData, ...updates };
};

export default function Home() {
  const [claimData, setClaimData] = useState<ClaimFormData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  // 1. 新增一个 state 来存储原始 JSON 响应
  const [rawJsonResponse, setRawJsonResponse] = useState<string | null>(null);

  // 此函数将传递给 UploadDocumentForm，用于处理文件上传
  const handleUpload = async (file: File) => {
    if (!file) return;

    setIsLoading(true);
    setClaimData(null);
    setRawJsonResponse(null); // 每次上传前清空旧的 JSON
    const toastId = toast.loading('正在上传并识别文件...');

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/infer", {
        method: "POST",
        body: formData,
      });

      // 2. 先获取原始文本响应
      const responseText = await response.text();
      // 存储原始 JSON 以便调试显示
      setRawJsonResponse(responseText);

      if (!response.ok) {
        throw new Error(`API 请求失败: ${response.status} ${responseText}`);
      }
      
      // 3. 使用已经获取的文本进行解析
      const data: ApiDataItem[] = JSON.parse(responseText);
      const transformedData = transformApiDataToFormData(data);
      setClaimData(transformedData);
      
      toast.success('识别成功！', { id: toastId });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error("上传或识别失败:", errorMessage);
      toast.error(`识别失败: ${errorMessage}`, { id: toastId });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Toaster position="top-center" />
      <div className="min-h-screen bg-gray-50 flex">
        <div className="max-w-2xl mx-auto py-12 px-4 sm:px-6 lg:px-8 flex-1 items-center justify-center">
          <div className="w-full">
            {/* 将 handleUpload 函数和 isLoading 状态传递给上传组件 */}
            <UploadDocumentForm onUpload={handleUpload} isUploading={isLoading} />
            
            {/* 4. 在上传组件下方，增加一个 div 来展示 DEBUG 的 JSON 数据 */}
            {rawJsonResponse && (
              <div className="mt-6 p-4 bg-gray-900 text-white rounded-lg shadow-md">
                <h3 className="text-lg font-semibold mb-2 border-b border-gray-700 pb-2">
                  API Raw JSON Response (Debug)
                </h3>
                <pre className="text-sm overflow-x-auto whitespace-pre-wrap break-all">
                  <code>
                    {/* 美化 JSON 格式以便阅读 */}
                    {JSON.stringify(JSON.parse(rawJsonResponse), null, 2)}
                  </code>
                </pre>
              </div>
            )}
          </div>
        </div>
        <div className="flex-1 flex flex-col lg:flex-row space-y-8 lg:space-y-0 lg:space-x-8">
          <div className="w-full">
            {/* 将识别出的数据传递给表单组件 */}
            <ClaimForm initialData={claimData} />
          </div>
        </div>
      </div>
    </>
  );
}
