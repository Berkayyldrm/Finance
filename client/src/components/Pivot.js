import axios from 'axios';
import React, { useEffect, useState } from 'react'
import PivotCard from './PivotCard';

function Pivot() {
    const [pivotData, setPivotData] = useState(null);
    useEffect(()=>{
        axios.get("http://localhost:8000/pivot/AEFES/2023-01-03/?period=1")
        .then(res => setPivotData(res.data));
    },[])
    console.log(pivotData);
    if(!pivotData){
        return <div>Yükleniyor</div>
    }
  return (
    <div className='col-12 d-flex justify-content-center flex-wrap gap-5'>
        <PivotCard pivotDetail={pivotData.pivot_points.camarilla} pivotTitle="Camarilla"/>
        <PivotCard pivotDetail={pivotData.pivot_points.classic} pivotTitle="Classic"/>
        <PivotCard pivotDetail={pivotData.pivot_points.woodie} pivotTitle="Woodie"/>
        <PivotCard pivotDetail={pivotData.pivot_points.fibonacci} pivotTitle="Fibonacci"/>
        <PivotCard pivotDetail={pivotData.pivot_points.demark} pivotTitle="Demark"/>
    </div>
  )
}

export default Pivot