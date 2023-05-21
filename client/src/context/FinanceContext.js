import { createContext, useEffect, useState } from "react";
import axios from "axios";
const FinanceContext = createContext();

export const FinanceProvider = ({ children }) => {
    const [selectCompany,setSelectCompany] = useState("");
    const [data,setData] = useState([]);
    useEffect(()=>{
      axios.get("http://localhost:8000/data/get_table_names")
      .then(res => setData(res.data.table_names))
    },[])
    const values = {
        selectCompany,
        setSelectCompany,
        data,
        setData
    };

  return <FinanceContext.Provider value={values}>{children}</FinanceContext.Provider>;
};

export default FinanceContext;