"use client"

import type { FormData } from "./claim-form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Shield } from "lucide-react"

interface Step2Props {
  formData: FormData
  updateFormData: (updates: Partial<FormData>) => void
}

export default function Step2({ formData, updateFormData }: Step2Props) {
  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Shield className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-800">授權同意查詢聲明書</h2>
        </div>
        <p className="text-sm text-gray-600">為了處理您的理賠申請，我們需要您的授權同意查詢相關醫療資料</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">被保險人基本資料</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="authInsuredName">被保險人姓名 *</Label>
            <Input
              id="authInsuredName"
              value={formData.authInsuredName}
              onChange={(e) => updateFormData({ authInsuredName: e.target.value })}
              placeholder="授權同意查詢聲明書上的被保險人姓名"
              required
            />
          </div>
          <div>
            <Label htmlFor="authInsuredIdNumber">被保險人身分證字號 *</Label>
            <Input
              id="authInsuredIdNumber"
              value={formData.authInsuredIdNumber}
              onChange={(e) => updateFormData({ authInsuredIdNumber: e.target.value })}
              placeholder="授權同意查詢聲明書上的被保險人身分證號碼"
              required
            />
          </div>
          <div>
            <Label htmlFor="authInsuredDob">被保險人出生年月日 *</Label>
            <Input
              id="authInsuredDob"
              type="date"
              value={formData.authInsuredDob}
              onChange={(e) => updateFormData({ authInsuredDob: e.target.value })}
              required
            />
          </div>
          <div>
            <Label htmlFor="authContractEffectiveDate">契約生效日 *</Label>
            <Input
              id="authContractEffectiveDate"
              type="date"
              value={formData.authContractEffectiveDate}
              onChange={(e) => updateFormData({ authContractEffectiveDate: e.target.value })}
              required
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">理賠相關資料</CardTitle>
        </CardHeader>
        <CardContent>
          <div>
            <Label htmlFor="authAilmentOrInjury">病名/傷害 *</Label>
            <Textarea
              id="authAilmentOrInjury"
              value={formData.authAilmentOrInjury}
              onChange={(e) => updateFormData({ authAilmentOrInjury: e.target.value })}
              placeholder="此次申請理賠相關的疾病或傷害名稱"
              rows={3}
              required
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-blue-700">立同意書人資料</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="authConsentingPersonName">立同意書人簽名 *</Label>
              <Input
                id="authConsentingPersonName"
                value={formData.authConsentingPersonName}
                onChange={(e) => updateFormData({ authConsentingPersonName: e.target.value })}
                placeholder="立同意書人(被保險人或其法定代理人)姓名"
                required
              />
            </div>
            <div>
              <Label htmlFor="authConsentingPersonIdNumber">立同意書人身分證字號 *</Label>
              <Input
                id="authConsentingPersonIdNumber"
                value={formData.authConsentingPersonIdNumber}
                onChange={(e) => updateFormData({ authConsentingPersonIdNumber: e.target.value })}
                placeholder="立同意書人的身分證號碼"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="authLegalGuardianSignatureName">法定代理人簽名</Label>
              <Input
                id="authLegalGuardianSignatureName"
                value={formData.authLegalGuardianSignatureName}
                onChange={(e) => updateFormData({ authLegalGuardianSignatureName: e.target.value })}
                placeholder="若立同意書人為未成年，其法定代理人姓名"
              />
            </div>
            <div>
              <Label htmlFor="authLegalGuardianIdNumber">法定代理人身分證字號</Label>
              <Input
                id="authLegalGuardianIdNumber"
                value={formData.authLegalGuardianIdNumber}
                onChange={(e) => updateFormData({ authLegalGuardianIdNumber: e.target.value })}
                placeholder="法定代理人的身分證號碼"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="authDate">同意日期 *</Label>
            <Input
              id="authDate"
              type="date"
              value={formData.authDate}
              onChange={(e) => updateFormData({ authDate: e.target.value })}
              required
            />
          </div>
        </CardContent>
      </Card>

      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="text-sm text-blue-800 space-y-2">
            <h4 className="font-semibold">授權聲明：</h4>
            <p>
              本人同意貴公司為審核本次理賠申請之需要，得向相關醫療院所、政府機關或其他機構查詢、
              蒐集本人之相關資料，並同意該等機構提供相關資料予貴公司。
            </p>
            <p>本授權書之效力以本次理賠申請案件之審核為限，審核完畢後自動失效。</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
