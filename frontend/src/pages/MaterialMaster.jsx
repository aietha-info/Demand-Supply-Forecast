/* import { useState } from "react";

export default function MaterialMaster() {
  const [formData, setFormData] = useState({
    Product_ID: "",
    Product_Description: "",
    Cat: "",
    Sub_Cat: "",
    Old_Product_ID: "",
    Product_Type: "",
    Is_Plannable: "",
    ABC_Cat: "",
    NLV: "",
    Lead_Time: "",
    Min_Lot_Size: "",
    Max_Lot_Size: "",
  });

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Saved:", formData);
  };

  const handleExcelUpload = (e) => {
    const file = e.target.files[0];
    if (file) console.log("Excel File:", file.name);
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h2 className="text-2xl font-bold mb-6">Material Master Form</h2>

      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4 max-w-4xl">
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className="block font-medium mb-1">{key.replaceAll("_", " ")}</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          </div>
        ))}

        <div className="col-span-2 flex gap-4 mt-4">
          <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded">Save</button>
          <button type="reset" className="bg-gray-500 text-white px-6 py-2 rounded">Cancel</button>
          <input type="file" accept=".xlsx, .xls" onChange={handleExcelUpload} className="border px-4 py-2 rounded" />
        </div>
      </form>
    </div>
  );
}
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as XLSX from "xlsx";

export default function MaterialMaster() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("single");
  const [formData, setFormData] = useState({
    Product_ID: "",
    Product_Description: "",
    Cat: "",
    Sub_Cat: "",
    Old_Product_ID: "",
    Product_Type: "",
    Is_Plannable: "",
    ABC_Cat: "",
    NLV: "",
    Lead_Time: "",
    Min_Lot_Size: "",
    Max_Lot_Size: "",
  });
  const [errors, setErrors] = useState({});
  const [editingId, setEditingId] = useState(null);
  const [uploadedData, setUploadedData] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");
  const [fileName, setFileName] = useState("");
  const [materials, setMaterials] = useState([
    {
      id: "MAT-001",
      description: "Premium Steel Coil",
      category: "Raw Material",
      subCategory: "Metals",
      type: "Standard",
      abcCategory: "A",
      status: "Active",
      Product_ID: "MAT-001",
      Product_Description: "Premium Steel Coil",
      Cat: "Raw Material",
      Sub_Cat: "Metals",
      Old_Product_ID: "OLD-MAT-001",
      Product_Type: "Raw Material",
      Is_Plannable: "Yes",
      ABC_Cat: "A",
      NLV: "1500",
      Lead_Time: "15",
      Min_Lot_Size: "100",
      Max_Lot_Size: "1000",
    },
    {
      id: "MAT-002",
      description: "Plastic Polymer Pellets",
      category: "Raw Material",
      subCategory: "Polymers",
      type: "Standard",
      abcCategory: "B",
      status: "Active",
      Product_ID: "MAT-002",
      Product_Description: "Plastic Polymer Pellets",
      Cat: "Raw Material",
      Sub_Cat: "Polymers",
      Old_Product_ID: "OLD-MAT-002",
      Product_Type: "Raw Material",
      Is_Plannable: "Yes",
      ABC_Cat: "B",
      NLV: "800",
      Lead_Time: "10",
      Min_Lot_Size: "50",
      Max_Lot_Size: "500",
    }
  ]);

  // Validation rules
  const validationRules = {
    Product_ID: {
      required: true,
      pattern: /^[A-Za-z0-9_-]+$/,
      message: "Product ID is required and can only contain letters, numbers, hyphens, and underscores"
    },
    Product_Description: {
      required: true,
      minLength: 3,
      maxLength: 100,
      message: "Product Description is required and must be between 3-100 characters"
    },
    Cat: {
      required: true,
      message: "Category is required"
    },
    Sub_Cat: {
      required: true,
      message: "Sub Category is required"
    },
    Product_Type: {
      required: true,
      message: "Product Type is required"
    },
    Is_Plannable: {
      required: true,
      message: "Plannable status is required"
    },
    ABC_Cat: {
      required: true,
      message: "ABC Category is required"
    },
    NLV: {
      required: true,
      pattern: /^\d+(\.\d{1,2})?$/,
      message: "NLV must be a valid number (e.g., 1500 or 1500.50)"
    },
    Lead_Time: {
      required: true,
      pattern: /^\d+$/,
      min: 0,
      max: 365,
      message: "Lead Time must be a whole number between 0-365 days"
    },
    Min_Lot_Size: {
      required: true,
      pattern: /^\d+$/,
      min: 1,
      message: "Min Lot Size must be a whole number greater than 0"
    },
    Max_Lot_Size: {
      required: true,
      pattern: /^\d+$/,
      min: 1,
      message: "Max Lot Size must be a whole number greater than 0"
    }
  };

  const validateField = (name, value) => {
    const rules = validationRules[name];
    if (!rules) return ""; // No validation rules for this field

    if (rules.required && !value.trim()) {
      return `${name.replaceAll("_", " ")} is required`;
    }

    if (rules.pattern && value && !rules.pattern.test(value)) {
      return rules.message;
    }

    if (rules.minLength && value.length < rules.minLength) {
      return `${name.replaceAll("_", " ")} must be at least ${rules.minLength} characters`;
    }

    if (rules.maxLength && value.length > rules.maxLength) {
      return `${name.replaceAll("_", " ")} must not exceed ${rules.maxLength} characters`;
    }

    if (rules.min !== undefined && value && parseInt(value) < rules.min) {
      return `${name.replaceAll("_", " ")} must be at least ${rules.min}`;
    }

    if (rules.max !== undefined && value && parseInt(value) > rules.max) {
      return `${name.replaceAll("_", " ")} must not exceed ${rules.max}`;
    }

    // Validate Min_Lot_Size vs Max_Lot_Size
    if (name === "Min_Lot_Size" && formData.Max_Lot_Size) {
      if (parseInt(value) > parseInt(formData.Max_Lot_Size)) {
        return "Min Lot Size cannot be greater than Max Lot Size";
      }
    }

    if (name === "Max_Lot_Size" && formData.Min_Lot_Size) {
      if (parseInt(value) < parseInt(formData.Min_Lot_Size)) {
        return "Max Lot Size cannot be less than Min Lot Size";
      }
    }

    return "";
  };

  const validateForm = () => {
    const newErrors = {};
    let isValid = true;

    Object.keys(validationRules).forEach(field => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    // Clear error when user starts typing
    if (errors[name]) {
      const error = validateField(name, value);
      if (error) {
        setErrors({ ...errors, [name]: error });
      } else {
        const newErrors = { ...errors };
        delete newErrors[name];
        setErrors(newErrors);
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      // Scroll to first error
      const firstErrorField = Object.keys(errors)[0];
      const element = document.querySelector(`[name="${firstErrorField}"]`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.focus();
      }
      return;
    }
    
    if (editingId) {
      // Update existing material
      setMaterials(materials.map(material => 
        material.id === editingId 
          ? { ...material, ...formData, description: formData.Product_Description }
          : material
      ));
      setEditingId(null);
    } else {
      // Add new material
      const newMaterial = {
        id: `MAT-${String(materials.length + 1).padStart(3, '0')}`,
        description: formData.Product_Description,
        category: formData.Cat,
        subCategory: formData.Sub_Cat,
        type: formData.Product_Type,
        abcCategory: formData.ABC_Cat,
        status: "Active",
        ...formData
      };
      setMaterials([...materials, newMaterial]);
    }
    
    // Reset form and errors
    setFormData({
      Product_ID: "",
      Product_Description: "",
      Cat: "",
      Sub_Cat: "",
      Old_Product_ID: "",
      Product_Type: "",
      Is_Plannable: "",
      ABC_Cat: "",
      NLV: "",
      Lead_Time: "",
      Min_Lot_Size: "",
      Max_Lot_Size: "",
    });
    setErrors({});
  };

  const handleEdit = (material) => {
    setFormData({
      Product_ID: material.Product_ID,
      Product_Description: material.Product_Description,
      Cat: material.Cat,
      Sub_Cat: material.Sub_Cat,
      Old_Product_ID: material.Old_Product_ID,
      Product_Type: material.Product_Type,
      Is_Plannable: material.Is_Plannable,
      ABC_Cat: material.ABC_Cat,
      NLV: material.NLV,
      Lead_Time: material.Lead_Time,
      Min_Lot_Size: material.Min_Lot_Size,
      Max_Lot_Size: material.Max_Lot_Size,
    });
    setEditingId(material.id);
    setActiveTab("single");
    setErrors({});
    // Scroll to form
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = (materialId) => {
    if (window.confirm("Are you sure you want to delete this material?")) {
      setMaterials(materials.filter(material => material.id !== materialId));
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setFormData({
      Product_ID: "",
      Product_Description: "",
      Cat: "",
      Sub_Cat: "",
      Old_Product_ID: "",
      Product_Type: "",
      Is_Plannable: "",
      ABC_Cat: "",
      NLV: "",
      Lead_Time: "",
      Min_Lot_Size: "",
      Max_Lot_Size: "",
    });
    setErrors({});
  };

  const handleReset = () => {
    setFormData({
      Product_ID: "",
      Product_Description: "",
      Cat: "",
      Sub_Cat: "",
      Old_Product_ID: "",
      Product_Type: "",
      Is_Plannable: "",
      ABC_Cat: "",
      NLV: "",
      Lead_Time: "",
      Min_Lot_Size: "",
      Max_Lot_Size: "",
    });
    setErrors({});
  };

  const handleExcelUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setUploadStatus("processing");

    const reader = new FileReader();
    
    reader.onload = (event) => {
      try {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        
        // Get first worksheet
        const worksheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[worksheetName];
        
        // Convert to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        if (jsonData.length < 2) {
          setUploadStatus("error");
          setUploadedData([]);
          return;
        }

        // Get headers (first row)
        const headers = jsonData[0];
        
        // Process data rows
        const processedData = jsonData.slice(1).map((row, index) => {
          const rowData = {};
          headers.forEach((header, colIndex) => {
            if (header && row[colIndex] !== undefined) {
              // Convert header to proper format (remove spaces, handle special chars)
              const formattedHeader = header.trim().replace(/\s+/g, '_');
              rowData[formattedHeader] = row[colIndex];
            }
          });
          
          // Add ID if not present
          if (!rowData.Product_ID) {
            rowData.Product_ID = `UPLOAD-${String(index + 1).padStart(3, '0')}`;
          }
          
          return rowData;
        }).filter(row => Object.keys(row).length > 0); // Remove empty rows

        setUploadedData(processedData);
        setUploadStatus("success");
        
      } catch (error) {
        console.error("Error processing Excel file:", error);
        setUploadStatus("error");
        setUploadedData([]);
      }
    };

    reader.onerror = () => {
      setUploadStatus("error");
      setUploadedData([]);
    };

    reader.readAsArrayBuffer(file);
  };

  const handleImportData = () => {
    if (uploadedData.length === 0) return;

    const newMaterials = uploadedData.map((data, index) => {
      const newId = `MAT-${String(materials.length + index + 1).padStart(3, '0')}`;
      
      return {
        id: newId,
        description: data.Product_Description || "",
        category: data.Cat || "",
        subCategory: data.Sub_Cat || "",
        type: data.Product_Type || "",
        abcCategory: data.ABC_Cat || "",
        status: "Active",
        Product_ID: data.Product_ID || newId,
        Product_Description: data.Product_Description || "",
        Cat: data.Cat || "",
        Sub_Cat: data.Sub_Cat || "",
        Old_Product_ID: data.Old_Product_ID || "",
        Product_Type: data.Product_Type || "",
        Is_Plannable: data.Is_Plannable || "Yes",
        ABC_Cat: data.ABC_Cat || "C",
        NLV: data.NLV || "0",
        Lead_Time: data.Lead_Time || "0",
        Min_Lot_Size: data.Min_Lot_Size || "1",
        Max_Lot_Size: data.Max_Lot_Size || "1000",
      };
    });

    setMaterials([...materials, ...newMaterials]);
    setUploadedData([]);
    setFileName("");
    setUploadStatus("");
    
    // Show success message
    alert(`Successfully imported ${newMaterials.length} materials!`);
    
    // Switch to browse tab to see the imported data
    setActiveTab("browse");
  };

  const handleClearUpload = () => {
    setUploadedData([]);
    setFileName("");
    setUploadStatus("");
    // Clear file input
    const fileInput = document.getElementById('file-upload');
    if (fileInput) fileInput.value = '';
  };

  const downloadTemplate = () => {
    // Create template data
    const templateData = [
      ["Product_ID", "Product_Description", "Cat", "Sub_Cat", "Old_Product_ID", "Product_Type", "Is_Plannable", "ABC_Cat", "NLV", "Lead_Time", "Min_Lot_Size", "Max_Lot_Size"],
      ["MAT-101", "Sample Material 1", "Raw Material", "Metals", "OLD-101", "Raw Material", "Yes", "A", "1000", "15", "50", "500"],
      ["MAT-102", "Sample Material 2", "Raw Material", "Polymers", "OLD-102", "Raw Material", "Yes", "B", "800", "10", "25", "250"]
    ];

    const ws = XLSX.utils.aoa_to_sheet(templateData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Template");
    
    // Download the file
    XLSX.writeFile(wb, "material_master_template.xlsx");
  };

  const productTypes = ["Finished Good", "Raw Material", "Semi-Finished", "Trading Good"];
  const abcCategories = ["A", "B", "C"];
  const planningOptions = ["Yes", "No"];

  const isFormValid = Object.keys(errors).length === 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50/30">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => navigate("/data-management")}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-2"
              >
                <span>←</span>
                <span>Back to Data Management</span>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Material Master</h1>
                <p className="text-gray-600">Manage product catalog, specifications, and material data</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center space-x-2">
                <span>📊</span>
                <span>Generate Report</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: "single", name: "Single Entry", icon: "➕" },
                { id: "bulk", name: "Bulk Import", icon: "📥" },
                { id: "browse", name: "Browse Materials", icon: "📋" }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-2 font-medium text-sm border-b-2 transition-colors duration-200 flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? "border-blue-500 text-blue-600"
                      : "border-transparent text-gray-500 hover:text-gray-700"
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Single Entry Form */}
          {activeTab === "single" && (
            <div className="p-8">
              <div className="flex items-center space-x-3 mb-6">
                <div className="p-2 rounded-lg bg-blue-100 text-blue-600">
                  <span className="text-xl">{editingId ? "✏️" : "➕"}</span>
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {editingId ? "Edit Material" : "Add New Material"}
                  </h2>
                  <p className="text-gray-600">
                    {editingId ? "Update material details" : "Enter material details manually"}
                  </p>
                </div>
              </div>

              {/* Validation Summary */}
              {Object.keys(errors).length > 0 && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center space-x-2 text-red-800 mb-2">
                    <span>⚠️</span>
                    <span className="font-semibold">Please fix the following errors:</span>
                  </div>
                  <ul className="list-disc list-inside text-red-700 text-sm space-y-1">
                    {Object.values(errors).map((error, index) => (
                      <li key={index}>{error}</li>
                    ))}
                  </ul>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Object.keys(formData).map((key) => (
                    <div key={key} className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">
                        {key.replaceAll("_", " ")}
                        {validationRules[key]?.required && <span className="text-red-500 ml-1">*</span>}
                      </label>
                      {key === "Product_Type" ? (
                        <div>
                          <select
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            className={`w-full border rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 transition-colors duration-200 ${
                              errors[key] ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                            }`}
                          >
                            <option value="">Select Type</option>
                            {productTypes.map(type => (
                              <option key={type} value={type}>{type}</option>
                            ))}
                          </select>
                          {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]}</p>}
                        </div>
                      ) : key === "ABC_Cat" ? (
                        <div>
                          <select
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            className={`w-full border rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 transition-colors duration-200 ${
                              errors[key] ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                            }`}
                          >
                            <option value="">Select Category</option>
                            {abcCategories.map(cat => (
                              <option key={cat} value={cat}>{cat}</option>
                            ))}
                          </select>
                          {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]}</p>}
                        </div>
                      ) : key === "Is_Plannable" ? (
                        <div>
                          <select
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            className={`w-full border rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 transition-colors duration-200 ${
                              errors[key] ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                            }`}
                          >
                            <option value="">Select Option</option>
                            {planningOptions.map(opt => (
                              <option key={opt} value={opt}>{opt}</option>
                            ))}
                          </select>
                          {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]}</p>}
                        </div>
                      ) : (
                        <div>
                          <input
                            type="text"
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            className={`w-full border rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 transition-colors duration-200 ${
                              errors[key] ? 'border-red-500' : 'border-gray-300 focus:border-blue-500'
                            }`}
                            placeholder={`Enter ${key.replaceAll("_", " ").toLowerCase()}`}
                          />
                          {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]}</p>}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="flex items-center space-x-4 pt-6 border-t border-gray-200">
                  <button 
                    type="submit" 
                    className={`px-8 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center space-x-2 ${
                      isFormValid 
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                    }`}
                    disabled={!isFormValid}
                  >
                    <span>{editingId ? "💾" : "➕"}</span>
                    <span>{editingId ? "Update Material" : "Save Material"}</span>
                  </button>
                  {editingId && (
                    <button 
                      type="button"
                      onClick={handleCancelEdit}
                      className="bg-gray-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-600 transition-colors duration-200 flex items-center space-x-2"
                    >
                      <span>❌</span>
                      <span>Cancel Edit</span>
                    </button>
                  )}
                  <button 
                    type="button"
                    onClick={handleReset}
                    className="bg-gray-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-600 transition-colors duration-200 flex items-center space-x-2"
                  >
                    <span>↺</span>
                    <span>Reset Form</span>
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Bulk Import Tab */}
          {activeTab === "bulk" && (
            <div className="p-8">
              <div className="flex items-center space-x-3 mb-6">
                <div className="p-2 rounded-lg bg-green-100 text-green-600">
                  <span className="text-xl">📥</span>
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Bulk Import Materials</h2>
                  <p className="text-gray-600">Upload Excel file with multiple material records</p>
                </div>
              </div>

              {/* Upload Section */}
              <div className="border-2 border-dashed border-gray-300 rounded-2xl p-12 text-center hover:border-blue-300 transition-colors duration-200 mb-8">
                <div className="text-6xl mb-4">📤</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Excel File</h3>
                <p className="text-gray-600 mb-6 max-w-md mx-auto">
                  Supported formats: .xlsx, .xls. Download the template file for correct formatting.
                </p>
                
                <input 
                  type="file" 
                  accept=".xlsx, .xls" 
                  onChange={handleExcelUpload} 
                  className="hidden" 
                  id="file-upload"
                />
                <label 
                  htmlFor="file-upload"
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 inline-flex items-center space-x-2 cursor-pointer"
                >
                  <span>📁</span>
                  <span>Choose File</span>
                </label>
                
                {fileName && (
                  <div className="mt-4">
                    <p className="text-green-600 font-medium">Selected file: {fileName}</p>
                  </div>
                )}

                {uploadStatus === "processing" && (
                  <div className="mt-4">
                    <p className="text-blue-600">Processing file...</p>
                  </div>
                )}

                {uploadStatus === "error" && (
                  <div className="mt-4">
                    <p className="text-red-600">Error processing file. Please check the format and try again.</p>
                  </div>
                )}
              </div>

              {/* Uploaded Data Preview */}
              {uploadedData.length > 0 && (
                <div className="bg-gray-50 rounded-2xl p-6 mb-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Preview Uploaded Data ({uploadedData.length} records)
                    </h3>
                    <div className="flex space-x-3">
                      <button
                        onClick={handleImportData}
                        className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors duration-200 flex items-center space-x-2"
                      >
                        <span>✅</span>
                        <span>Import All</span>
                      </button>
                      <button
                        onClick={handleClearUpload}
                        className="bg-gray-500 text-white px-6 py-2 rounded-lg font-semibold hover:bg-gray-600 transition-colors duration-200 flex items-center space-x-2"
                      >
                        <span>❌</span>
                        <span>Clear</span>
                      </button>
                    </div>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead className="bg-gray-50">
                          <tr>
                            {Object.keys(uploadedData[0] || {}).map((key) => (
                              <th key={key} className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                                {key.replaceAll("_", " ")}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                          {uploadedData.slice(0, 5).map((row, index) => (
                            <tr key={index} className="hover:bg-gray-50 transition-colors duration-150">
                              {Object.values(row).map((value, cellIndex) => (
                                <td key={cellIndex} className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">
                                  {value || "-"}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    {uploadedData.length > 5 && (
                      <div className="bg-gray-50 px-4 py-3 text-center text-sm text-gray-600">
                        Showing first 5 of {uploadedData.length} records
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Template Section */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                <div className="text-center p-4">
                  <div className="text-2xl mb-2">📋</div>
                  <div className="font-medium text-gray-900 mb-1">Download Template</div>
                  <div className="text-sm text-gray-600 mb-2">Get standardized Excel template</div>
                  <button
                    onClick={downloadTemplate}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors duration-200"
                  >
                    Download
                  </button>
                </div>
                <div className="text-center p-4">
                  <div className="text-2xl mb-2">🔍</div>
                  <div className="font-medium text-gray-900">Validate Data</div>
                  <div className="text-sm text-gray-600">Check for formatting errors</div>
                </div>
                <div className="text-center p-4">
                  <div className="text-2xl mb-2">⚡</div>
                  <div className="font-medium text-gray-900">Quick Import</div>
                  <div className="text-sm text-gray-600">Fast batch processing</div>
                </div>
              </div>
            </div>
          )}

          {/* Browse Materials Tab */}
          {activeTab === "browse" && (
            <div className="p-8">
              <div className="flex items-center space-x-3 mb-6">
                <div className="p-2 rounded-lg bg-purple-100 text-purple-600">
                  <span className="text-xl">📋</span>
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Material Catalog</h2>
                  <p className="text-gray-600">Browse and manage existing materials</p>
                </div>
              </div>

              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Material ID</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Description</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Category</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Type</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">ABC Category</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {materials.map((material, index) => (
                      <tr key={index} className="hover:bg-gray-50 transition-colors duration-150">
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">{material.Product_ID}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{material.Product_Description}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{material.Cat}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{material.Product_Type}</td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            material.ABC_Cat === 'A' ? 'bg-red-100 text-red-800' :
                            material.ABC_Cat === 'B' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {material.ABC_Cat}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            {material.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleEdit(material)}
                              className="text-blue-600 hover:text-blue-800 transition-colors duration-200 p-1 rounded hover:bg-blue-50"
                              title="Edit"
                            >
                              <span className="text-lg">✏️</span>
                            </button>
                            <button
                              onClick={() => handleDelete(material.id)}
                              className="text-red-600 hover:text-red-800 transition-colors duration-200 p-1 rounded hover:bg-red-50"
                              title="Delete"
                            >
                              <span className="text-lg">🗑️</span>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}