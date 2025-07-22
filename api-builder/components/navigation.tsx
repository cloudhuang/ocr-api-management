"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Plus, List } from "lucide-react";
import Link from "next/link";

export default function Navigation() {
  const router = useRouter();

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-8">
          <h1 className="text-xl font-bold">
            <Link href={"/"}>API Manager</Link>
          </h1>
          <div className="flex space-x-4">
            <Button
              variant="ghost"
              className="flex items-center gap-2"
              onClick={() => router.push("/")}
            >
              <List className="h-4 w-4" />
              API List
            </Button>
            <Button
              variant="ghost"
              className="flex items-center gap-2"
              onClick={() => router.push("/apis")}
            >
              <Plus className="h-4 w-4" />
              Create API
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
