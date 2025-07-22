"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Navigation from "@/components/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, Upload } from "lucide-react";

export default function OcrTestPage() {
  const router = useRouter();
  const [apiCode, setApiCode] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!apiCode.trim()) {
      setMessage("请输入 API CODE");
      return;
    }
    
    if (!selectedFile) {
      setMessage("请选择图片文件");
      return;
    }
    
    setLoading(true);
    setMessage("");
    setResult(null);
    
    try {
      const formData = new FormData();
      formData.append("api_code", apiCode);
      formData.append("image", selectedFile);
      
      const response = await fetch("/api/ocr", {
        method: "POST",
        body: formData,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
        setMessage("OCR 处理成功");
      } else {
        setMessage(data.error || "OCR 处理失败");
      }
    } catch (error) {
      console.error("OCR 处理错误:", error);
      setMessage("网络错误，请稍后重试");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
 
      <div className="max-w-4xl mx-auto p-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold">OCR 测试</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="api-code">API CODE</Label>
                <Input
                  id="api-code"
                  value={apiCode}
                  onChange={(e) => setApiCode(e.target.value)}
                  placeholder="输入 API CODE"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="image">图片文件</Label>
                <div className="flex items-center gap-2">
                  <Input
                    id="image"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                    className="flex items-center gap-2"
                  >
                    <Upload className="h-4 w-4" />
                    选择图片
                  </Button>
                  <span className="text-sm text-gray-500">
                    {selectedFile ? selectedFile.name : "未选择文件"}
                  </span>
                </div>
              </div>
              
              <Button type="submit" disabled={loading} className="w-full">
                {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {loading ? "处理中..." : "开始 OCR 处理"}
              </Button>
            </form>
            
            {message && (
              <Alert className={`mt-6 ${message.includes("成功") ? "border-green-200 bg-green-50" : ""}`}>
                <AlertDescription className={message.includes("成功") ? "text-green-800" : "text-red-600"}>
                  {message}
                </AlertDescription>
              </Alert>
            )}
            
            {result && (
              <div className="mt-6 space-y-4">
                <h3 className="text-lg font-medium">处理结果</h3>
                <div className="bg-gray-100 p-4 rounded-md">
                  <pre className="whitespace-pre-wrap text-sm">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}