"use client"

import type { FormData } from "./claim-form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Checkbox } from "@/components/ui/checkbox"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface Step1Props {
  formData: FormData
  updateFormData: (updates: Partial<FormData>) => void
}

export default function Step1({ formData, updateFormData }: Step1Props) {
  const handleClaimTypeChange = (claimType: string, checked: boolean) => {
    const currentTypes = formData.claimType || []
    if (checked) {
      updateFormData({ claimType: [...currentTypes, claimType] })
    } else {
      updateFormData({ claimType: currentTypes.filter((type) => type !== claimType) })
    }
  }

  return (
    <div className="space-y-8">
      {/* 事故人基本資料 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">事故人基本資料</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="insuredName">事故人姓名 *</Label>
            <Input
              id="insuredName"
              value={formData.insuredName}
              onChange={(e) => updateFormData({ insuredName: e.target.value })}
              placeholder="需要理賠的被保險人/事故人全名"
              required
            />
          </div>
          <div>
            <Label htmlFor="insuredIdNumber">事故人身分證字號 *</Label>
            <Input
              id="insuredIdNumber"
              value={formData.insuredIdNumber}
              onChange={(e) => updateFormData({ insuredIdNumber: e.target.value })}
              placeholder="被保險人/事故人的身分證號碼"
              required
            />
          </div>
          <div>
            <Label htmlFor="insuredDateOfBirth">出生日期 *</Label>
            <Input
              id="insuredDateOfBirth"
              type="date"
              value={formData.insuredDateOfBirth}
              onChange={(e) => updateFormData({ insuredDateOfBirth: e.target.value })}
              required
            />
          </div>
          <div>
            <Label htmlFor="currentOccupation">目前職業/工作內容</Label>
            <Input
              id="currentOccupation"
              value={formData.currentOccupation}
              onChange={(e) => updateFormData({ currentOccupation: e.target.value })}
              placeholder="請詳述職業與主要工作內容"
            />
          </div>
          <div>
            <Label htmlFor="occupationCode">職業代碼</Label>
            <Input
              id="occupationCode"
              value={formData.occupationCode}
              onChange={(e) => updateFormData({ occupationCode: e.target.value })}
              placeholder="若不清楚可留白"
            />
          </div>
          <div className="md:col-span-2">
            <Label htmlFor="mailingAddress">通訊處 *</Label>
            <Input
              id="mailingAddress"
              value={formData.mailingAddress}
              onChange={(e) => updateFormData({ mailingAddress: e.target.value })}
              placeholder="用於接收理賠相關文件的郵寄地址"
              required
            />
          </div>
        </CardContent>
      </Card>

      {/* 保險資料 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">保險資料</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="policyNumber">保單號碼 *</Label>
              <Input
                id="policyNumber"
                value={formData.policyNumber}
                onChange={(e) => updateFormData({ policyNumber: e.target.value })}
                placeholder="申請理賠的保單號碼"
                required
              />
            </div>
            <div>
              <Label htmlFor="policyholderUnit">要保單位</Label>
              <Input
                id="policyholderUnit"
                value={formData.policyholderUnit}
                onChange={(e) => updateFormData({ policyholderUnit: e.target.value })}
                placeholder="僅在申請團體保險時需要填寫"
              />
            </div>
          </div>

          <div>
            <Label>險別 *</Label>
            <RadioGroup
              value={formData.insuranceType}
              onValueChange={(value) => updateFormData({ insuranceType: value })}
              className="flex flex-wrap gap-4 mt-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="個人險" id="insurance-1" />
                <Label htmlFor="insurance-1">個人險</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="團體險" id="insurance-2" />
                <Label htmlFor="insurance-2">團體險</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="旅行平安險" id="insurance-3" />
                <Label htmlFor="insurance-3">旅行平安險</Label>
              </div>
            </RadioGroup>
          </div>

          <div>
            <Label>理賠型態 (可複選)</Label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
              {["醫療", "重大疾病", "失能", "身故", "意外傷害", "住院", "豁免保費"].map((type) => (
                <div key={type} className="flex items-center space-x-2">
                  <Checkbox
                    id={`claim-${type}`}
                    checked={formData.claimType?.includes(type) || false}
                    onCheckedChange={(checked) => handleClaimTypeChange(type, checked as boolean)}
                  />
                  <Label htmlFor={`claim-${type}`}>{type}</Label>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 事故詳情 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">事故詳情</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label>事故原因 *</Label>
            <RadioGroup
              value={formData.incidentCause}
              onValueChange={(value) => updateFormData({ incidentCause: value })}
              className="flex gap-4 mt-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="1" id="cause-1" />
                <Label htmlFor="cause-1">意外</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="2" id="cause-2" />
                <Label htmlFor="cause-2">疾病</Label>
              </div>
            </RadioGroup>
          </div>

          <div>
            <Label>事故地區 *</Label>
            <RadioGroup
              value={formData.incidentRegion}
              onValueChange={(value) => updateFormData({ incidentRegion: value })}
              className="flex gap-4 mt-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="01" id="region-01" />
                <Label htmlFor="region-01">國內</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="02" id="region-02" />
                <Label htmlFor="region-02">大陸</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="03" id="region-03" />
                <Label htmlFor="region-03">國外</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="incidentDateTime">事故時間 *</Label>
              <Input
                id="incidentDateTime"
                type="datetime-local"
                value={formData.incidentDateTime}
                onChange={(e) => updateFormData({ incidentDateTime: e.target.value })}
                required
              />
            </div>
            <div>
              <Label htmlFor="incidentLocation">事故地點 *</Label>
              <Input
                id="incidentLocation"
                value={formData.incidentLocation}
                onChange={(e) => updateFormData({ incidentLocation: e.target.value })}
                required
              />
            </div>
          </div>

          <div>
            <Label htmlFor="incidentDetails">經過詳情 *</Label>
            <Textarea
              id="incidentDetails"
              value={formData.incidentDetails}
              onChange={(e) => updateFormData({ incidentDetails: e.target.value })}
              required
            />
          </div>

          <div>
            <Label htmlFor="hospitalsVisited">曾就診之醫院診所</Label>
            <Textarea
              id="hospitalsVisited"
              value={formData.hospitalsVisited}
              onChange={(e) => updateFormData({ hospitalsVisited: e.target.value })}
              placeholder="列出與此次事故相關曾經就診的所有醫院或診所名稱"
              rows={2}
            />
          </div>
        </CardContent>
      </Card>

      {/* 憲警單位資料 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">憲警單位資料 (交通意外事故)</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="policeOfficerName">員警姓名</Label>
            <Input
              id="policeOfficerName"
              value={formData.policeOfficerName}
              onChange={(e) => updateFormData({ policeOfficerName: e.target.value })}
            />
          </div>
          <div>
            <Label htmlFor="policeContactPhone">聯絡電話</Label>
            <Input
              id="policeContactPhone"
              value={formData.policeContactPhone}
              onChange={(e) => updateFormData({ policeContactPhone: e.target.value })}
            />
          </div>
          <div className="md:col-span-2">
            <Label htmlFor="handlingPoliceUnit">處理憲警單位</Label>
            <Input
              id="handlingPoliceUnit"
              value={formData.handlingPoliceUnit}
              onChange={(e) => updateFormData({ handlingPoliceUnit: e.target.value })}
            />
          </div>
        </CardContent>
      </Card>

      {/* 聯絡資料 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">聯絡資料</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="contactAddress">聯絡地址</Label>
            <Input
              id="contactAddress"
              value={formData.contactAddress}
              onChange={(e) => updateFormData({ contactAddress: e.target.value })}
              placeholder="完整的聯絡地址"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="mobilePhone">行動電話 *</Label>
              <Input
                id="mobilePhone"
                type="tel"
                value={formData.mobilePhone}
                onChange={(e) => updateFormData({ mobilePhone: e.target.value })}
                placeholder="主要聯絡人手機號碼"
                required
              />
            </div>
            <div>
              <Label htmlFor="landlinePhone">聯絡市話</Label>
              <Input
                id="landlinePhone"
                type="tel"
                value={formData.landlinePhone}
                onChange={(e) => updateFormData({ landlinePhone: e.target.value })}
                placeholder="主要聯絡人市內電話"
              />
            </div>
            <div>
              <Label htmlFor="email">電子郵件</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => updateFormData({ email: e.target.value })}
                placeholder="用於接收電子通知書的Email"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 申請人資料 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">申請人資料</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="applicantSignatureName">申請人/受益人簽名 *</Label>
              <Input
                id="applicantSignatureName"
                value={formData.applicantSignatureName}
                onChange={(e) => updateFormData({ applicantSignatureName: e.target.value })}
                placeholder="申請人或受益人姓名"
                required
              />
            </div>
            <div>
              <Label htmlFor="applicantIdNumber">申請人/受益人身分證字號 *</Label>
              <Input
                id="applicantIdNumber"
                value={formData.applicantIdNumber}
                onChange={(e) => updateFormData({ applicantIdNumber: e.target.value })}
                placeholder="申請人或受益人的身分證號碼"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="legalGuardianName">法定代理人/監護人/輔助人</Label>
              <Input
                id="legalGuardianName"
                value={formData.legalGuardianName}
                onChange={(e) => updateFormData({ legalGuardianName: e.target.value })}
                placeholder="若申請人為未成年或受監護宣告者填寫"
              />
            </div>
            <div>
              <Label htmlFor="legalGuardianIdNumber">法定代理人身分證字號</Label>
              <Input
                id="legalGuardianIdNumber"
                value={formData.legalGuardianIdNumber}
                onChange={(e) => updateFormData({ legalGuardianIdNumber: e.target.value })}
                placeholder="法定代理人的身分證號碼"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="applicationDate">申請日期 *</Label>
            <Input
              id="applicationDate"
              type="date"
              value={formData.applicationDate}
              onChange={(e) => updateFormData({ applicationDate: e.target.value })}
              required
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
