"use client"

import { useState, useEffect } from "react"
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
  description: string
  project: string
  tags: string[]
  responseFormat: "markdown" | "json"
  createdAt: string
  status: "active" | "inactive" | "draft"
}

export default function ApiList() {
  const [searchTerm, setSearchTerm] = useState("")
  const [apis, setApis] = useState<ApiItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  
  // 从后端 API 获取数据
  const fetchApis = async () => {
    try {
      setLoading(true)
      setError("")
      
      const response = await fetch("/api/apis")
      
      if (!response.ok) {
        throw new Error("Failed to fetch APIs")
      }
      
      const data = await response.json()
      
      // 转换后端数据格式为前端组件需要的格式
      const formattedApis = data.map((api: any) => {
        // 从 definition 中提取数据
        const definition = api.definition || {}
        
        return {
          id: api.id.toString(),
          apiCode: definition.apiCode || "",
          apiName: api.name || definition.apiName || "",
          description: api.description || definition.description || "",
          project: definition.project || "",
          tags: definition.tags || [],
          responseFormat: definition.responseFormat || "json",
          createdAt: api.created_at ? new Date(api.created_at).toLocaleDateString() : "Unknown",
          status: "active" // 默认状态，后端可能没有这个字段
        }
      })
      
      setApis(formattedApis)
    } catch (err) {
      console.error("Error fetching APIs:", err)
      setError("Failed to load APIs. Please try again later.")
    } finally {
      setLoading(false)
    }
  }
  
  // 组件加载时获取数据
  useEffect(() => {
    fetchApis()
  }, [])

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
    router.push(`/apis/${id}/edit`)
  }

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this API?")) {
      try {
        const response = await fetch(`/api/apis/${id}`, {
          method: "DELETE",
        })
        
        if (!response.ok) {
          throw new Error("Failed to delete API")
        }
        
        // 从本地状态中移除已删除的 API
        setApis(apis.filter((api) => api.id !== id))
        console.log("API deleted successfully:", id)
      } catch (err) {
        console.error("Error deleting API:", err)
        alert("Failed to delete API. Please try again.")
      }
    }
  }

  const handleView = (id: string) => {
    console.log("View API:", id)
    router.push(`/apis/${id}`)
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

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-500">Loading APIs...</p>
            </div>
          )}
          
          {/* Error State */}
          {error && !loading && (
            <div className="text-center py-12">
              <div className="text-red-500 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Error</h3>
              <p className="text-gray-500 mb-4">{error}</p>
              <Button onClick={fetchApis}>
                Try Again
              </Button>
            </div>
          )}
          
          {/* API Table */}
          {!loading && !error && (
            <div className="border rounded-lg">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>API Code</TableHead>
                    <TableHead>API Name</TableHead>
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
          )}

          {/* Empty State */}
          {!loading && !error && filteredApis.length === 0 && (
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
