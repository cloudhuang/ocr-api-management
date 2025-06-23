import ClaimForm from "@/components/claim-form";
import UploadDocumentForm from "@/components/upload-document-form";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      <div className="max-w-2xl mx-auto py-12 px-4 sm:px-6 lg:px-8 flex-1 items-center justify-center">
        <div className="w-full">
          <UploadDocumentForm />
        </div>

      </div>
      <div className="flex-1 flex flex-col lg:flex-row space-y-8 lg:space-y-0 lg:space-x-8">
        <div className="w-full">
          <ClaimForm />
        </div>
      </div>
    </div>
  );
}
