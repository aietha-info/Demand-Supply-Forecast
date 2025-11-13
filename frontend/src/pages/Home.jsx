/* import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const features = [
    { title: "Data Management", path: "/data-management" },
    { title: "Demand Planning", path: "/demand-planning" },
    { title: "Demand Scheduling", path: "/demand-scheduling" },
    { title: "Distribution Planning", path: "/distribution-planning" },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-8">Planning System</h1>
      <div className="grid grid-cols-2 gap-6">
        {features.map((f) => (
          <button
            key={f.title}
            onClick={() => navigate(f.path)}
            className="bg-blue-600 text-white px-8 py-4 rounded-xl shadow hover:bg-blue-700"
          >
            {f.title}
          </button>
        ))}
      </div>
    </div>
  );
}
 */


import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  
  const features = [
    { 
      title: "Data Management", 
      path: "/data-management",
      description: "Centralized data repository for demand and supply information",
      icon: "📊",
      gradient: "from-blue-500 to-cyan-500"
    },
    { 
      title: "Demand Planning", 
      path: "/demand-planning",
      description: "Forecast customer demand and optimize inventory levels",
      icon: "📈",
      gradient: "from-green-500 to-emerald-500"
    },
    { 
      title: "Supply Planning", 
      path: "/supply-planning",
      description: "Manage supplier networks and production schedules",
      icon: "🏭",
      gradient: "from-orange-500 to-red-500"
    },
    { 
      title: "Distribution Planning", 
      path: "/distribution-planning",
      description: "Optimize logistics and distribution networks",
      icon: "🚚",
      gradient: "from-purple-500 to-pink-500"
    },
  ];

  const stats = [
    { value: "99%", label: "Forecast Accuracy" },
    { value: "24/7", label: "Real-time Monitoring" },
    { value: "50%", label: "Cost Reduction" },
    { value: "95%", label: "On-time Delivery" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200">
      {/* Header Section */}
      <div className="relative bg-gradient-to-r from-blue-900 to-purple-800 text-white py-20">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">Supply Chain Intelligence Platform</h1>
          <p className="text-xl mb-8 text-blue-100">
            Optimize your demand and supply operations with AI-powered planning
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="text-2xl font-bold text-white">{stat.value}</div>
                <div className="text-blue-100 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Core Modules</h2>
          <p className="text-gray-600 text-lg">
            Comprehensive tools for end-to-end supply chain management
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8 mb-16">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden group cursor-pointer"
              onClick={() => navigate(feature.path)}
            >
              <div className={`h-2 bg-gradient-to-r ${feature.gradient}`}></div>
              <div className="p-8">
                <div className="flex items-center mb-4">
                  <span className="text-3xl mr-4">{feature.icon}</span>
                  <h3 className="text-2xl font-bold text-gray-800">{feature.title}</h3>
                </div>
                <p className="text-gray-600 mb-6">{feature.description}</p>
                <div className="flex justify-between items-center">
                  <span className="text-blue-600 font-semibold group-hover:text-blue-800 transition-colors">
                    Explore Module →
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Stats Table */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            Performance Overview
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Metric</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Current</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Target</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Trend</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-800">Inventory Turnover</td>
                  <td className="px-6 py-4 text-sm font-semibold text-green-600">8.2x</td>
                  <td className="px-6 py-4 text-sm text-gray-600">9.0x</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      ↗ Improving
                    </span>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-800">Forecast Accuracy</td>
                  <td className="px-6 py-4 text-sm font-semibold text-blue-600">94%</td>
                  <td className="px-6 py-4 text-sm text-gray-600">95%</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      → Stable
                    </span>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-800">Order Fill Rate</td>
                  <td className="px-6 py-4 text-sm font-semibold text-emerald-600">98.5%</td>
                  <td className="px-6 py-4 text-sm text-gray-600">99%</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                      ↗ Improving
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-12">
          <button 
            onClick={() => navigate("/dashboard")}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Launch Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}