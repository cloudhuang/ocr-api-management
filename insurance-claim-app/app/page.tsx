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

const codeToField: Record<string, keyof ClaimFormData> = {
  insuredName: "insuredName",
  mailingAddress: "mailingAddress",
  insuredIdNumber: "insuredIdNumber",
  insuredBirthDate: "insuredBirthDate",
  policyHolder: "policyHolder",
  currentOccupation: "currentOccupation",
  occupationCode: "occupationCode",
  policyNumber: "policyNumber",
  insuranceType: "insuranceType",
  claimType: "claimType",
  incidentCause: "incidentCause",
  incidentRegion: "incidentRegion",
  hospitalsVisited: "hospitalsVisited",
  accidentDate: "accidentDate",
  accidentLocation: "accidentLocation",
  accidentDescription: "accidentDescription",
  policeName: "policeName",
  policeContact: "policeContact",
  policeUnit: "policeUnit",
  beneficiaryName: "beneficiaryName",
  beneficiaryIdNumber: "beneficiaryIdNumber",
  beneficiaryAccount: "beneficiaryAccount",
  bankAccount: "bankAccount",
  bankAccountCode: "bankAccountCode",
  accountNumber: "accountNumber",
  contactAddress: "contactAddress",
  mobilePhone: "mobilePhone",
  email: "email",
  landlinePhone: "landlinePhone",
  applicantSignatureName: "applicantSignatureName",
  applicantIdNumber: "applicantIdNumber",
  legalGuardianName: "legalGuardianName",
  legalGuardianIdNumber: "legalGuardianIdNumber",
  applicationDate: "applicationDate",
  authInsuredName: "authInsuredName",
  authInsuredDob: "authInsuredDob",
  authInsuredIdNumber: "authInsuredIdNumber",
  authContractEffectiveDate: "authContractEffectiveDate",
  authAilmentOrInjury: "authAilmentOrInjury",
  authConsentingPersonName: "authConsentingPersonName",
  authConsentingPersonIdNumber: "authConsentingPersonIdNumber",
  authLegalGuardianSignatureName: "authLegalGuardianSignatureName",
  authLegalGuardianIdNumber: "authLegalGuardianIdNumber",
  authDate: "authDate",
};

// 数据转换函数：将 API 数组转换为表单所需的扁平对象
const transformApiDataToFormData = (apiData: ApiDataItem[]): ClaimFormData => {
  const defaultFormData: ClaimFormData = {
    insuredName: "", mailingAddress: "", insuredIdNumber: "", insuredBirthDate: "",
    policyHolder: "", currentOccupation: "", occupationCode: "", policyNumber: "",
    insuranceType: "", claimType: [], incidentCause: "", incidentRegion: "",
    hospitalsVisited: "", accidentDate: "", accidentLocation: "", accidentDescription: "",
    policeName: "", policeContact: "", policeUnit: "", beneficiaryName: "",
    beneficiaryIdNumber: "", beneficiaryAccount: "", bankAccount: "", bankAccountCode: "",
    accountNumber: "", contactAddress: "", mobilePhone: "", email: "", landlinePhone: "",
    applicantSignatureName: "", applicantIdNumber: "", legalGuardianName: "",
    legalGuardianIdNumber: "", applicationDate: "", authInsuredName: "", authInsuredDob: "",
    authInsuredIdNumber: "", authContractEffectiveDate: "", authAilmentOrInjury: "",
    authConsentingPersonName: "", authConsentingPersonIdNumber: "",
    authLegalGuardianSignatureName: "", authLegalGuardianIdNumber: "", authDate: "",
  };
  const updates: Partial<ClaimFormData> = {};
  apiData.forEach(item => {
    const key = codeToField[item.code];
    if (!key) return;
    if (key === 'claimType' && typeof item.value === 'string') {
      updates[key] = item.value.split(',').map(s => s.trim()).filter(Boolean);
    } else {
      updates[key] = item.value as any;
    }
  });
  return { ...defaultFormData, ...updates };
};

export default function Home() {
  const [claimData, setClaimData] = useState<ClaimFormData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // 此函数将传递给 UploadDocumentForm，用于处理文件上传
  const handleUpload = async (file: File) => {
    if (!file) return;

    setIsLoading(true);
    setClaimData(null); 
    const toastId = toast.loading('正在上传并识别文件...');

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/infer_openai", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API 请求失败: ${response.status} ${errorText}`);
      }

      const data: ApiDataItem[] = await response.json();
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
