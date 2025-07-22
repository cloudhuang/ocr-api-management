"use client";

import { useState } from "react"
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Plus, X, Loader2 } from "lucide-react";

interface Rule {
  id: string;
  text: string;
}

interface Tag {
  id: string;
  text: string;
  color: string;
}

export default function ApiBuilder() {
  const router = useRouter()
  const [apiCode, setApiCode] = useState("");
  const [apiName, setApiName] = useState("");
  const [apiPath, setApiPath] = useState("");
  const [description, setDescription] = useState("");
  const [project, setProject] = useState("");
  const [responseFormat, setResponseFormat] = useState("markdown");
  const [jsonStructure, setJsonStructure] = useState("");
  const [newRule, setNewRule] = useState("");
  const [newTag, setNewTag] = useState("");

  const [rules, setRules] = useState<Rule[]>([
    { id: "1", text: 'the date format should be "yyyy-MM-dd"' },
    { id: "2", text: "Please return in English" },
  ]);

  const [tags, setTags] = useState<Tag[]>([
    { id: "1", text: "TAG", color: "bg-green-200 text-green-800" },
    { id: "2", text: "TAG", color: "bg-yellow-200 text-yellow-800" },
  ]);

  const addRule = () => {
    if (newRule.trim()) {
      const rule: Rule = {
        id: Date.now().toString(),
        text: newRule.trim(),
      };
      setRules([...rules, rule]);
      setNewRule("");
    }
  };

  const deleteRule = (id: string) => {
    setRules(rules.filter((rule) => rule.id !== id));
  };

  const addTag = () => {
    if (newTag.trim()) {
      const colors = [
        "bg-blue-200 text-blue-800",
        "bg-green-200 text-green-800",
        "bg-yellow-200 text-yellow-800",
        "bg-purple-200 text-purple-800",
        "bg-pink-200 text-pink-800",
      ];
      const tag: Tag = {
        id: Date.now().toString(),
        text: newTag.trim(),
        color: colors[Math.floor(Math.random() * colors.length)],
      };
      setTags([...tags, tag]);
      setNewTag("");
    }
  };

  const deleteTag = (id: string) => {
    setTags(tags.filter((tag) => tag.id !== id));
  };

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSave = async () => {
    if (!apiName.trim()) {
      setMessage("请输入 API 名称");
      return;
    }

    setLoading(true);
    setMessage("");

    const apiData = {
      apiCode,
      apiName,
      apiPath,
      description,
      project,
      tags: tags.map((tag) => tag.text),
      rules: rules.map((rule) => rule.text),
      responseFormat,
      jsonStructure: responseFormat === "json" ? jsonStructure : null,
    };

    try {
      const response = await fetch("/api/apis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(apiData),
      });

      if (response.ok) {
        const result = await response.json();
        setMessage("API 定义保存成功！");
        console.log("保存成功:", result);
        
        // 显示成功消息后短暂延迟，然后跳转到 API List 页面
        setTimeout(() => {
          router.push("/");
        }, 1500); // 1.5秒后跳转，让用户有时间看到成功消息
      } else {
        const errorData = await response.json();
        setMessage(errorData.error || "保存失败");
      }
    } catch (error) {
      console.error("保存错误:", error);
      setMessage("网络错误，请稍后重试");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    // 直接跳转到 API List 页面
    router.push("/");
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">API Builder</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* API Builder Input */}
          <div className="space-y-2">
            <Label htmlFor="api-code" className="text-sm font-medium">
              API CODE
            </Label>
            <Input
              id="api-code"
              value={apiCode}
              onChange={(e) => setApiCode(e.target.value)}
              className="w-full"
            />
          </div>

          {/* API Name */}
          <div className="space-y-2">
            <Label htmlFor="api-name" className="text-sm font-medium">
              API NAME
            </Label>
            <Input
              id="api-name"
              value={apiName}
              onChange={(e) => setApiName(e.target.value)}
              className="w-full"
            />
          </div>

          {/* API Path */}
          <div className="space-y-2">
            <Label htmlFor="api-path" className="text-sm font-medium">
              API PATH
            </Label>
            <Input
              id="api-path"
              value={apiPath}
              onChange={(e) => setApiPath(e.target.value)}
              className="w-full"
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description" className="text-sm font-medium">
              DESCRIPTION
            </Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full min-h-[100px]"
            />
          </div>

          {/* Project */}
          <div className="space-y-2">
            <Label htmlFor="project" className="text-sm font-medium">
              Project
            </Label>
            <Input
              id="project"
              value={project}
              onChange={(e) => setProject(e.target.value)}
              className="w-full"
            />
          </div>

          {/* Tags */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">TAGS</Label>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <Badge
                  key={tag.id}
                  variant="secondary"
                  className={`${tag.color} relative pr-8`}
                >
                  {tag.text}
                  <button
                    onClick={() => deleteTag(tag.id)}
                    className="absolute right-1 top-1/2 -translate-y-1/2 hover:bg-black/10 rounded-full p-0.5"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Add new tag"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addTag()}
                className="flex-1"
              />
              <Button onClick={addTag} size="sm">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Rules */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium">RULES</Label>
              <Button onClick={addRule} size="sm" variant="outline">
                ADD
              </Button>
            </div>

            <div className="space-y-2">
              {rules.map((rule) => (
                <div key={rule.id} className="flex items-center gap-2">
                  <Input
                    value={rule.text}
                    onChange={(e) => {
                      setRules(
                        rules.map((r) =>
                          r.id === rule.id ? { ...r, text: e.target.value } : r
                        )
                      );
                    }}
                    className="flex-1"
                  />
                  <Button
                    onClick={() => deleteRule(rule.id)}
                    size="sm"
                    variant="outline"
                    className="text-red-600 hover:text-red-700"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>

            <div className="flex gap-2">
              <Input
                placeholder="Enter new rule"
                value={newRule}
                onChange={(e) => setNewRule(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addRule()}
                className="flex-1"
              />
            </div>
          </div>

          {/* Response Format */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">RESPONSE FORMAT</Label>
            <RadioGroup
              value={responseFormat}
              onValueChange={setResponseFormat}
              className="flex gap-6"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="markdown" id="markdown" />
                <Label htmlFor="markdown">markdown</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="json" id="json" />
                <Label htmlFor="json">JSON</Label>
              </div>
            </RadioGroup>
          </div>

          {/* JSON Structure */}
          {responseFormat === "json" && (
            <div className="space-y-2">
              <Label htmlFor="json-structure" className="text-sm font-medium">
                JSON Structure
              </Label>
              <Textarea
                id="json-structure"
                value={jsonStructure}
                onChange={(e) => setJsonStructure(e.target.value)}
                placeholder="Enter JSON structure here..."
                className="w-full min-h-[200px] font-mono"
              />
            </div>
          )}

          {/* Message Display */}
          {message && (
            <Alert
              className={
                message.includes("成功") ? "border-green-200 bg-green-50" : ""
              }
            >
              <AlertDescription
                className={
                  message.includes("成功") ? "text-green-800" : "text-red-600"
                }
              >
                {message}
              </AlertDescription>
            </Alert>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end gap-4 pt-6">
            <Button variant="outline" onClick={handleCancel} disabled={loading}>
              cancel
            </Button>
            <Button onClick={handleSave} disabled={loading}>
              {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {loading ? "保存中..." : "save"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
