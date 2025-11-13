import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import DataManagement from "../pages/DataManagement";
import MaterialMaster from "../pages/MaterialMaster";
import DemandPlanning from "../pages/DemandPlanning";
import DemandScheduling from "../pages/DemandScheduling";
import DistributionPlanning from "../pages/DistributionPlanning";

export default function AppRoutes() {
  return (
    
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/data-management" element={<DataManagement />} />
        <Route path="/data-management/material-master" element={<MaterialMaster />} />
        <Route path="/demand-planning" element={<DemandPlanning />} />
        <Route path="/demand-scheduling" element={<DemandScheduling />} />
        <Route path="/distribution-planning" element={<DistributionPlanning />} />
      </Routes>
  
  );
}
