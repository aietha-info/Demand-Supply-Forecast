/* import { useNavigate } from "react-router-dom";

export default function DataManagement() {
  const navigate = useNavigate();
  const items = [
    { title: "Material Master", path: "/data-management/material-master" },
    { title: "Manage Sales History" },
    { title: "Inventory Management" },
    { title: "Region Management" },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-2xl font-bold mb-8">Data Management</h1>
      <div className="grid grid-cols-2 gap-6">
        {items.map((i) => (
          <button
            key={i.title}
            onClick={() => i.path && navigate(i.path)}
            className="bg-green-600 text-white px-8 py-4 rounded-xl shadow hover:bg-green-700"
          >
            {i.title}
          </button>
        ))}
      </div>
    </div>
  );
}
 */

import { useNavigate } from "react-router-dom";

export default function DataManagement() {
  const navigate = useNavigate();
  
  const modules = [
    { 
      title: "Material Master", 
      path: "/data-management/material-master",
      description: "Manage product catalog, specifications, and material data including imports",
      icon: "📦",
      count: "1,247 Items",
      status: "Active",
      gradient: "from-blue-500 to-cyan-500",
      features: ["Import Data", "Export Templates", "Bulk Updates"]
    },
    { 
      title: "Sales History", 
      path: "/data-management/sales-history",
      description: "Analyze historical sales data and customer trends",
      icon: "📊",
      count: "45.2K Records",
      status: "Updated Today",
      gradient: "from-green-500 to-emerald-500",
      features: ["Trend Analysis", "Seasonal Patterns", "Customer Insights"]
    },
    { 
      title: "Inventory Management", 
      path: "/data-management/inventory",
      description: "Real-time inventory tracking and stock optimization",
      icon: "🏪",
      count: "156 Locations",
      status: "Live Monitoring",
      gradient: "from-orange-500 to-amber-500",
      features: ["Stock Levels", "Reorder Points", "Warehouse Management"]
    },
    { 
      title: "Region Management", 
      path: "/data-management/regions",
      description: "Configure geographic regions and distribution networks",
      icon: "🌍",
      count: "28 Regions",
      status: "Configured",
      gradient: "from-purple-500 to-pink-500",
      features: ["Zone Setup", "Distribution Centers", "Territory Mapping"]
    }
  ];

  const recentActivities = [
    { action: "Data Import", description: "Material master records imported", time: "2 min ago", status: "completed", module: "Material Master" },
    { action: "Data Sync", description: "Sales data updated from ERP", time: "1 hour ago", status: "completed", module: "Sales History" },
    { action: "Stock Count", description: "Inventory cycle count completed", time: "3 hours ago", status: "completed", module: "Inventory Management" },
    { action: "Region Update", description: "New distribution zone added", time: "5 hours ago", status: "completed", module: "Region Management" },
  ];

  const dataStats = [
    { label: "Total Records", value: "2.4M", change: "+12.4%", icon: "📁" },
    { label: "Data Quality", value: "98.3%", change: "+2.1%", icon: "✅" },
    { label: "Import Success", value: "99.8%", change: "+0.3%", icon: "📥" },
    { label: "Active Sources", value: "24", change: "+2", icon: "🔗" },
  ];

  const importActions = [
    { name: "Bulk Import", description: "Upload multiple records via CSV/Excel", format: "CSV, XLSX" },
    { name: "Template Download", description: "Get standardized import templates", format: "Excel Template" },
    { name: "API Integration", description: "Connect external systems automatically", format: "REST API" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50/30">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => navigate("/")}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-2"
              >
                <span>←</span>
                <span>Back to Home</span>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Data Management</h1>
                <p className="text-gray-600">Centralized data governance and master data management</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200 flex items-center space-x-2">
                <span>📤</span>
                <span>Export Report</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {dataStats.map((stat, index) => (
            <div key={index} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow duration-200">
              <div className="flex items-center space-x-4">
                <div className="text-2xl">{stat.icon}</div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <div className="flex items-baseline space-x-2 mt-1">
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {stat.change}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Modules Grid */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Data Management Modules</h2>
                <span className="text-sm text-gray-500">{modules.length} core modules</span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {modules.map((module, index) => (
                  <div
                    key={module.title}
                    onClick={() => module.path && navigate(module.path)}
                    className="group cursor-pointer transform transition-all duration-300 hover:scale-[1.02]"
                  >
                    <div className="bg-gradient-to-br from-white to-gray-50/50 rounded-xl border-2 border-gray-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-300 h-full">
                      <div className="flex items-start space-x-4">
                        <div className={`p-3 rounded-xl bg-gradient-to-r ${module.gradient} text-white shadow-md`}>
                          <span className="text-2xl">{module.icon}</span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                              {module.title}
                            </h3>
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              {module.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-4 leading-relaxed">{module.description}</p>
                          
                          {/* Features List */}
                          <div className="flex flex-wrap gap-2 mb-4">
                            {module.features.map((feature, idx) => (
                              <span key={idx} className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-gray-100 text-gray-700">
                                {feature}
                              </span>
                            ))}
                          </div>
                          
                          <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                            <span className="text-sm text-gray-500 font-medium">{module.count}</span>
                            <div className="flex items-center space-x-2 text-blue-600 group-hover:text-blue-800 transition-colors">
                              <span className="text-sm font-semibold">Access Module</span>
                              <span className="transform group-hover:translate-x-1 transition-transform">→</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Import Section under Material Master */}
            <div className="mt-8 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center space-x-3 mb-6">
                <div className="p-2 rounded-lg bg-blue-100 text-blue-600">
                  <span className="text-xl">📥</span>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">Data Import Center</h3>
                  <p className="text-gray-600">Available in Material Master module for bulk operations</p>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {importActions.map((action, index) => (
                  <div key={index} className="border-2 border-dashed border-gray-300 rounded-xl p-5 hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200 group cursor-pointer">
                    <div className="text-center">
                      <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">📥</div>
                      <h4 className="font-semibold text-gray-900 mb-2">{action.name}</h4>
                      <p className="text-sm text-gray-600 mb-3">{action.description}</p>
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                        {action.format}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-start space-x-3">
                  <div className="text-blue-600 mt-0.5">💡</div>
                  <div>
                    <p className="text-sm text-blue-800 font-medium">
                      Import functionality is available within the Material Master module
                    </p>
                    <p className="text-xs text-blue-600 mt-1">
                      Navigate to Material Master to access bulk import, template downloads, and data validation tools.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar - Recent Activities */}
          <div className="space-y-6">
            {/* Recent Activities */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activities</h3>
              <div className="space-y-4">
                {recentActivities.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                        <span className="text-xs text-gray-400">{activity.time}</span>
                      </div>
                      <p className="text-xs text-gray-600 mb-1">{activity.description}</p>
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700">
                        {activity.module}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Help */}
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
              <h3 className="text-lg font-semibold mb-4">Need Help?</h3>
              <div className="space-y-3">
                <button className="w-full text-left p-3 rounded-lg bg-white/10 hover:bg-white/20 transition-colors duration-200 flex items-center space-x-3">
                  <span>📚</span>
                  <span>View Documentation</span>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-white/10 hover:bg-white/20 transition-colors duration-200 flex items-center space-x-3">
                  <span>🎥</span>
                  <span>Watch Tutorials</span>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-white/10 hover:bg-white/20 transition-colors duration-200 flex items-center space-x-3">
                  <span>💬</span>
                  <span>Contact Support</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}