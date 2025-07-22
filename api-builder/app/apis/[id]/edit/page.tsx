"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import ApiBuilderEdit from "@/components/api-builder-edit";

export default function EditApiPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [apiData, setApiData] = useState(null);

  useEffect(() => {
    const fetchApiDetails = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/apis/${id}`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch API details");
        }
        
        const data = await response.json();
        setApiData(data);
      } catch (err) {
        console.error("Error fetching API details:", err);
        setError("Failed to load API details. Please try again later.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchApiDetails();
  }, [id]);

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

  if (error || !apiData) {
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
            <button 
              onClick={() => router.push("/")}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              Back to API List
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <ApiBuilderEdit apiData={apiData} apiId={id} />
    </div>
  );
}