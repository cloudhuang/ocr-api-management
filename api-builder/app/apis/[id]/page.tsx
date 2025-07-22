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
    apiPath: string;
    project: string;
    tags: string[];
    rules: string[];
    responseFormat: string;
    jsonStructure: string | null;
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
    <div className="min-h-screen bg-gray-50">
 
      <div className="max-w-4xl mx-auto p-6">
        <div className="mb-6 flex items-center justify-between">
          <Button variant="outline" onClick={() => router.push("/")} className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to API List
          </Button>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleEdit} className="flex items-center gap-2">
              <Edit className="h-4 w-4" />
              Edit
            </Button>
            <Button variant="outline" onClick={handleDelete} className="flex items-center gap-2 text-red-600 hover:text-red-700">
              <Trash2 className="h-4 w-4" />
              Delete
            </Button>
          </div>
        </div>

        <Card>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <div className="text-sm text-muted-foreground mb-1">API Code</div>
                <CardTitle className="text-2xl font-bold">{api.definition.apiCode}</CardTitle>
              </div>
              <Badge className="bg-green-100 text-green-800">Active</Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-2">API Name</h3>
              <p>{api.definition.apiName || api.name}</p>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">API Path</h3>
              <code className="bg-gray-100 px-3 py-2 rounded block text-sm">{api.definition.apiPath}</code>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">Description</h3>
              <p className="text-gray-700">{api.description || api.definition.description || "No description provided."}</p>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">Project</h3>
              <p>{api.definition.project || "Not specified"}</p>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {api.definition.tags && api.definition.tags.length > 0 ? (
                  api.definition.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary" className={getTagColor()}>
                      {tag}
                    </Badge>
                  ))
                ) : (
                  <p className="text-gray-500">No tags</p>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">Rules</h3>
              {api.definition.rules && api.definition.rules.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {api.definition.rules.map((rule, index) => (
                    <li key={index}>{rule}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No rules defined</p>
              )}
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">Response Format</h3>
              <Badge variant="outline" className="capitalize">
                {api.definition.responseFormat || "Not specified"}
              </Badge>
            </div>

            {api.definition.responseFormat === "json" && api.definition.jsonStructure && (
              <div>
                <h3 className="text-lg font-medium mb-2">JSON Structure</h3>
                <pre className="bg-gray-100 p-3 rounded overflow-auto max-h-80 text-sm">
                  {api.definition.jsonStructure}
                </pre>
              </div>
            )}

            <div>
              <h3 className="text-lg font-medium mb-2">Created At</h3>
              <p className="text-gray-700">
                {api.created_at ? new Date(api.created_at).toLocaleString() : "Unknown"}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}