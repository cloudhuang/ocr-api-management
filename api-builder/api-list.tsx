"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Search, Plus, MoreHorizontal, Edit, Trash2, Eye } from "lucide-react"

interface ApiItem {
  id: string
  apiCode: string
  apiName: string
  apiPath: string
  description: string
  project: string
  tags: string[]
  responseFormat: "markdown" | "json"
  createdAt: string
  status: "active" | "inactive" | "draft"
}

export default function ApiList() {
  const [searchTerm, setSearchTerm] = useState("")
  const [apis, setApis] = useState<ApiItem[]>([
    {
      id: "1",
      apiCode: "USER_001",
      apiName: "Get User Profile",
      apiPath: "/api/users/profile",
      description: "Retrieve user profile information including personal details and preferences",
      project: "User Management",
      tags: ["user", "profile", "authentication"],
      responseFormat: "json",
      createdAt: "2024-01-15",
      status: "active",
    },
    {
      id: "2",
      apiCode: "ORDER_002",
      apiName: "Create Order",
      apiPath: "/api/orders/create",
      description: "Create a new order with items and customer information",
      project: "E-commerce",
      tags: ["order", "payment", "e-commerce"],
      responseFormat: "json",
      createdAt: "2024-01-14",
      status: "active",
    },
    {
      id: "3",
      apiCode: "REPORT_003",
      apiName: "Generate Sales Report",
      apiPath: "/api/reports/sales",
      description: "Generate comprehensive sales reports with filtering options",
      project: "Analytics",
      tags: ["report", "analytics", "sales"],
      responseFormat: "markdown",
      createdAt: "2024-01-13",
      status: "draft",
    },
    {
      id: "4",
      apiCode: "AUTH_004",
      apiName: "User Authentication",
      apiPath: "/api/auth/login",
      description: "Authenticate user credentials and return access token",
      project: "Authentication",
      tags: ["auth", "security", "login"],
      responseFormat: "json",
      createdAt: "2024-01-12",
      status: "active",
    },
  ])

  const router = useRouter()

  const filteredApis = apis.filter(
    (api) =>
      api.apiName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      api.apiCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
      api.project.toLowerCase().includes(searchTerm.toLowerCase()) ||
      api.tags.some((tag) => tag.toLowerCase().includes(searchTerm.toLowerCase())),
  )

  const handleEdit = (id: string) => {
    console.log("Edit API:", id)
    // Navigate to edit page or open edit modal
  }

  const handleDelete = (id: string) => {
    setApis(apis.filter((api) => api.id !== id))
    console.log("Delete API:", id)
  }

  const handleView = (id: string) => {
    console.log("View API:", id)
    // Navigate to view page or open view modal
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800"
      case "inactive":
        return "bg-red-100 text-red-800"
      case "draft":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getTagColors = () => {
    const colors = [
      "bg-blue-100 text-blue-800",
      "bg-green-100 text-green-800",
      "bg-purple-100 text-purple-800",
      "bg-pink-100 text-pink-800",
      "bg-indigo-100 text-indigo-800",
    ]
    return colors[Math.floor(Math.random() * colors.length)]
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <Card className="max-w-7xl mx-auto">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-2xl font-bold">API Management</CardTitle>
              <p className="text-muted-foreground mt-1">Manage and monitor your APIs</p>
            </div>
            <Button className="flex items-center gap-2" onClick={() => router.push("/apis")}>
              <Plus className="h-4 w-4" />
              Create New API
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {/* Search Bar */}
          <div className="flex items-center gap-4 mb-6">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search APIs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="text-sm text-muted-foreground">
              {filteredApis.length} of {apis.length} APIs
            </div>
          </div>

          {/* API Table */}
          <div className="border rounded-lg">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>API Code</TableHead>
                  <TableHead>API Name</TableHead>
                  <TableHead>Path</TableHead>
                  <TableHead>Project</TableHead>
                  <TableHead>Tags</TableHead>
                  <TableHead>Format</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="w-[50px]">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredApis.map((api) => (
                  <TableRow key={api.id}>
                    <TableCell className="font-medium">{api.apiCode}</TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{api.apiName}</div>
                        <div className="text-sm text-muted-foreground truncate max-w-[200px]">{api.description}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <code className="bg-gray-100 px-2 py-1 rounded text-sm">{api.apiPath}</code>
                    </TableCell>
                    <TableCell>{api.project}</TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {api.tags.slice(0, 2).map((tag, index) => (
                          <Badge key={index} variant="secondary" className={getTagColors()}>
                            {tag}
                          </Badge>
                        ))}
                        {api.tags.length > 2 && (
                          <Badge variant="secondary" className="bg-gray-100 text-gray-600">
                            +{api.tags.length - 2}
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="capitalize">
                        {api.responseFormat}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(api.status)}>{api.status}</Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">{api.createdAt}</TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleView(api.id)}>
                            <Eye className="h-4 w-4 mr-2" />
                            View Details
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleEdit(api.id)}>
                            <Edit className="h-4 w-4 mr-2" />
                            Edit
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleDelete(api.id)} className="text-red-600">
                            <Trash2 className="h-4 w-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Empty State */}
          {filteredApis.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Search className="h-12 w-12 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No APIs found</h3>
              <p className="text-gray-500 mb-4">
                {searchTerm ? "Try adjusting your search terms" : "Get started by creating your first API"}
              </p>
              {!searchTerm && (
                <Button onClick={() => router.push("/apis")}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create New API
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
