"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import Step1 from "./step1"
import Step2 from "./step2"
import { ChevronLeft, ChevronRight, FileText } from "lucide-react"

export interface FormData {
  insuredName: string
  mailingAddress: string
  insuredIdNumber: string
  insuredDateOfBirth: string
  policyholderUnit: string
  currentOccupation: string
  occupationCode: string
  policyNumber: string
  insuranceType: string
  claimType: string
  incidentCause: string
  incidentRegion: string
  hospitalsVisited: string
  incidentDateTime: string
  incidentLocation: string
  incidentDetails: string
  policeOfficerName: string
  policeContactPhone: string
  handlingPoliceUnit: string
  beneficiaryName: string
  beneficiaryIdNumber: string
  paymentAccountOption: string
  bankNameAndBranch: string
  bankCode: string
  accountNumber: string
  contactAddress: string
  mobilePhone: string
  email: string
  landlinePhone: string
  applicantSignatureName: string
  applicantIdNumber: string
  legalGuardianName: string
  legalGuardianIdNumber: string
  applicationDate: string
  authInsuredName: string
  authInsuredDob: string
  authInsuredIdNumber: string
  authContractEffectiveDate: string
  authAilmentOrInjury: string
  authConsentingPersonName: string
  authConsentingPersonIdNumber: string
  authLegalGuardianSignatureName: string
  authLegalGuardianIdNumber: string
  authDate: string
}

// 1. 定义 props 接口，以接收外部数据
interface ClaimFormProps {
  initialData: FormData | null;
}

export default function ClaimForm({ initialData }: ClaimFormProps) {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<FormData>({
    insuredName: "",
    mailingAddress: "",
    insuredIdNumber: "",
    insuredDateOfBirth: "",
    policyholderUnit: "",
    currentOccupation: "",
    occupationCode: "",
    policyNumber: "",
    insuranceType: "",
    claimType: "",
    incidentCause: "",
    incidentRegion: "",
    hospitalsVisited: "",
    incidentDateTime: "",
    incidentLocation: "",
    incidentDetails: "",
    policeOfficerName: "",
    policeContactPhone: "",
    handlingPoliceUnit: "",
    beneficiaryName: "",
    beneficiaryIdNumber: "",
    paymentAccountOption: "",
    bankNameAndBranch: "",
    bankCode: "",
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
  })

  // 2. 使用 useEffect 钩子来监听外部数据的变化
  // 当 initialData prop 改变时 (即API调用成功后), 更新表单的内部状态
  useEffect(() => {
    if (initialData) {
      setFormData(prev => ({
        ...prev,
        ...initialData,
      }));
    }
  }, [initialData]);

  const totalSteps = 2
  const progress = (currentStep / totalSteps) * 100

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSubmit = () => {
    console.log("表單提交資料:", formData)
    alert("申請已提交！請查看控制台以檢視完整資料。")
  }

  const updateFormData = (updates: Partial<FormData>) => {
    setFormData((prev) => ({ ...prev, ...updates }))
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Card className="shadow-lg">
        <CardHeader className="text-center border-b">
          <div className="flex items-center justify-center gap-2 mb-4">
            <FileText className="h-8 w-8 text-blue-600" />
            <CardTitle className="text-2xl font-bold text-gray-800">保險理賠申請書</CardTitle>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600">
              <span>
                步驟 {currentStep} / {totalSteps}
              </span>
              <span>{currentStep === 1 ? "基本資料與事故詳情" : "授權同意書"}</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </CardHeader>

        <CardContent className="p-6">
          {currentStep === 1 && <Step1 formData={formData} updateFormData={updateFormData} />}
          {currentStep === 2 && <Step2 formData={formData} updateFormData={updateFormData} />}
        </CardContent>

        <div className="flex justify-between items-center p-6 border-t bg-gray-50">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentStep === 1}
            className="flex items-center gap-2"
          >
            <ChevronLeft className="h-4 w-4" />
            上一步
          </Button>

          <div className="flex gap-2">
            {Array.from({ length: totalSteps }, (_, i) => (
              <div key={i} className={`w-3 h-3 rounded-full ${i + 1 <= currentStep ? "bg-blue-600" : "bg-gray-300"}`} />
            ))}
          </div>

          {currentStep < totalSteps ? (
            <Button onClick={handleNext} className="flex items-center gap-2">
              下一步
              <ChevronRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700">
              提交申請
            </Button>
          )}
        </div>
      </Card>
    </div>
  )
}
