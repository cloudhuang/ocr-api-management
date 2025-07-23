"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/navigation";
import { ArrowLeft, Edit, Trash2 } from "lucide-react";

interface ApiDetails {
  id: string;
  name: string;
  description: string;
  definition: {
    apiCode: string;
    apiName: string;
    description?: string;
    project: string;
    tags: string[];
    rules: string[];
    responseFormat: string;
    jsonStructure: string | null;
    includeHandwriting?: boolean;
    responseLanguage?: string;
  };
  created_at: string;
}

export default function ApiDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [api, setApi] = useState<ApiDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchApiDetails = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/apis/${id}`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch API details");
        }
        
        const data = await response.json();
        setApi(data);
      } catch (err) {
        console.error("Error fetching API details:", err);
        setError("Failed to load API details. Please try again later.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchApiDetails();
  }, [id]);

  const handleEdit = () => {
    router.push(`/apis/${id}/edit`);
  };

  const handleDelete = async () => {
    if (confirm("Are you sure you want to delete this API?")) {
      try {
        const response = await fetch(`/api/apis/${id}`, {
          method: "DELETE",
        });
        
        if (!response.ok) {
          throw new Error("Failed to delete API");
        }
        
        router.push("/");
      } catch (err) {
        console.error("Error deleting API:", err);
        alert("Failed to delete API. Please try again.");
      }
    }
  };

  const getTagColor = () => {
    const colors = [
      "bg-blue-100 text-blue-800",
      "bg-green-100 text-green-800",
      "bg-purple-100 text-purple-800",
      "bg-pink-100 text-pink-800",
      "bg-indigo-100 text-indigo-800",
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">

        <div className="max-w-4xl mx-auto p-6">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-500">Loading API details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !api) {
    return (
      <div className="min-h-screen bg-gray-50">
  
        <div className="max-w-4xl mx-auto p-6">
          <div className="text-center py-12">
            <div className="text-red-500 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Error</h3>
            <p className="text-gray-500 mb-4">{error || "API not found"}</p>
            <Button onClick={() => router.push("/")}>
              Back to API List
            </Button>
          </div>
        </div>
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-3xl mx-auto py-10 px-4">
        {/* Header Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between bg-white rounded-xl shadow-sm px-6 py-5 border border-gray-200">
            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => router.push("/")} className="flex items-center gap-2 text-blue-600 hover:bg-blue-50 transition">
                <ArrowLeft className="h-5 w-5" />
                <span className="font-medium">Back</span>
              </Button>
              <span className="text-xs text-gray-400">|</span>
              <span className="text-lg font-semibold text-gray-800">API Details</span>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleEdit} className="flex items-center gap-2 border-blue-200 text-blue-700 hover:bg-blue-50 transition">
                <Edit className="h-4 w-4" />
                Edit
              </Button>
              <Button variant="outline" onClick={handleDelete} className="flex items-center gap-2 border-red-200 text-red-600 hover:bg-red-50 transition">
                <Trash2 className="h-4 w-4" />
                Delete
              </Button>
            </div>
          </div>
        </div>

        {/* Main Card Section */}
        <Card className="rounded-2xl shadow-md border border-gray-200">
          <CardHeader className="bg-blue-50 rounded-t-2xl px-6 py-5 border-b border-gray-100">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 w-full">
              <div className="flex flex-col gap-2">
                <div className="text-xs text-blue-700 font-semibold tracking-wide">API Code</div>
                <CardTitle className="text-3xl font-extrabold text-blue-900 leading-tight">{api.definition.apiCode}</CardTitle>
                <div className="mt-1 text-sm text-gray-500">{api.definition.apiName || api.name}</div>
                <div className="mt-2">
                  <span className="text-xs font-medium text-indigo-800 bg-indigo-400 p-2 rounded-md">Project: {api.definition.project || "Not specified"}</span>
                </div>
              </div>
              <Badge className="bg-green-100 text-green-800 px-3 py-1 rounded-full shadow-sm">Active</Badge>
            </div>
          </CardHeader>
          <CardContent className="px-6 py-8 space-y-8">
            {/* Description */}
            <div className="grid grid-cols-1 md:grid-cols-1 gap-8">
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">Description</h3>
                <p className="text-gray-800 text-sm leading-relaxed">{api.description || api.definition.description || "No description provided."}</p>
              </div>
            </div>

            {/* Tags & Rules */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {api.definition.tags && api.definition.tags.length > 0 ? (
                    api.definition.tags.map((tag, index) => (
                      <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full shadow-sm hover:bg-blue-200 transition">
                        {tag}
                      </Badge>
                    ))
                  ) : (
                    <p className="text-gray-400">No tags</p>
                  )}
                </div>
              </div>
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">Rules</h3>
                {api.definition.rules && api.definition.rules.length > 0 ? (
                  <ul className="list-disc pl-5 space-y-1 text-gray-800 text-sm">
                    {api.definition.rules.map((rule, index) => (
                      <li key={index}>{rule}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-400">No rules defined</p>
                )}
              </div>
            </div>

            {/* Handwriting Recognition & Response Language */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">手写体识别</h3>
                <Badge
                  variant="outline"
                  className={`px-3 py-1 shadow-sm ${
                    api.definition.includeHandwriting
                      ? "border border-green-200 text-green-700 bg-green-50"
                      : "border border-gray-200 text-gray-700 bg-gray-50"
                  }`}
                >
                  {api.definition.includeHandwriting ? "已启用" : "未启用"}
                </Badge>
              </div>
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">返回语言</h3>
                <Badge variant="outline" className="px-3 py-1 border border-purple-200 text-purple-700 bg-purple-50 shadow-sm">
                  {(() => {
                    switch (api.definition.responseLanguage) {
                      case "simplified_chinese": return "简体中文";
                      case "traditional_chinese": return "繁体中文";
                      case "japanese": return "日本語";
                      case "english":
                      default: return "English";
                    }
                  })()}
                </Badge>
              </div>
            </div>

            {/* Response Format & JSON Structure */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-base font-semibold mb-2 text-gray-700">Response Format</h3>
                <Badge variant="outline" className="capitalize px-3 py-1 border border-blue-200 text-blue-700 bg-blue-50 shadow-sm">
                  {api.definition.responseFormat || "Not specified"}
                </Badge>
              </div>
              {api.definition.responseFormat === "json" && api.definition.jsonStructure && (
                <div>
                  <h3 className="text-base font-semibold mb-2 text-gray-700">JSON Structure</h3>
                  <pre className="bg-gray-100 p-3 rounded-lg overflow-auto max-h-60 text-xs border border-gray-200 shadow-inner">
                    {api.definition.jsonStructure}
                  </pre>
                </div>
              )}
            </div>

            {/* Created At */}
            <div className="pt-4 border-t border-gray-100">
              <h3 className="text-base font-semibold mb-2 text-gray-700">Created At</h3>
              <p className="text-gray-700 text-sm">
                {api.created_at ? new Date(api.created_at).toLocaleString() : "Unknown"}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}