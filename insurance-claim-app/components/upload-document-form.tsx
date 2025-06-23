"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FileText, CheckCircle, XCircle } from "lucide-react";

interface FileWithPreview extends File {
  preview: string;
}

// 1. 定义 props 接口
interface UploadDocumentFormProps {
  onUpload: (file: File) => void;
  isUploading: boolean;
}

export default function UploadDocumentForm({ onUpload, isUploading }: UploadDocumentFormProps) {
  const [files, setFiles] = useState<FileWithPreview[]>([]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newFiles = Array.from(event.target.files || []).map((file) =>
      Object.assign(file, {
        preview: URL.createObjectURL(file),
      })
    );
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleUpload = () => {
    // 2. 当点击上传时，调用从 props 传入的 onUpload 函数
    // 我们只处理第一个文件，符合后端接口要求
    if (files.length > 0) {
      onUpload(files[0]);
    }
  };

  const handleRemoveFile = (fileToRemove: FileWithPreview) => {
    setFiles((prevFiles) =>
      prevFiles.filter((file) => file !== fileToRemove)
    );
    URL.revokeObjectURL(fileToRemove.preview);
  };

  return (
    <div className="max-w-4xl mx-auto p-8 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-8 text-center">Upload Documents</h2>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select files to upload
        </label>
        <Input
          type="file"
          multiple
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      {files.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Selected Files:</h3>
          <ul className="space-y-3">
            {files.map((file, index) => (
              <li
                key={index}
                className="flex items-center justify-between p-3 bg-gray-100 rounded-md"
              >
                <div className="flex items-center">
                  <FileText className="w-5 h-5 text-gray-500 mr-2" />
                  <span className="text-sm">{file.name}</span>
                </div>
                <button
                  onClick={() => handleRemoveFile(file)}
                  className="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <XCircle className="w-4 h-4" />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {files.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Image Previews:</h3>
          <div className="p-1">
            {files
              .filter((file) => file.type.startsWith("image/"))
              .map((file, index) => (
                <div key={index} className="relative p-1">
                  <img
                    src={file.preview}
                    alt={`Preview of ${file.name}`}
                    className="w-full h-64 object-cover rounded-md"
                  />
                  <button
                    onClick={() => handleRemoveFile(file)}
                    className="absolute top-2 right-2 bg-white rounded-full p-1 text-red-500 hover:text-red-700 focus:outline-none"
                  >
                    <XCircle className="w-4 h-4" />
                  </button>
                </div>
              ))}
          </div>
        </div>
      )}

      <div className="flex justify-end space-x-3">
        <Button
          onClick={handleUpload}
          // 3. 使用 props 传入的 isUploading 状态
          disabled={isUploading || files.length === 0}
          className="bg-blue-500 hover:bg-blue-600 px-6 py-3"
        >
          {isUploading ? "Uploading..." : "Upload Documents"}
        </Button>
      </div>
    </div>
  );
}
