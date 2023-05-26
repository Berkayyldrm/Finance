import React from 'react'

function PivotCard({pivotDetail,pivotTitle}) {
  return (
    <div className='col-5 border'>
    <p className='fs-6 fw-bold border-bottom text-center'>{pivotTitle}</p>
    <div className='col-12 d-flex justify-content-between'>
        <div className='col-6'>
            <p className='fs-7 fw-semibold text-center'>Current Price</p>
            <hr className='col-8 mx-auto'/>
            <p className='text-center'>{pivotDetail.current_price.toFixed(2)}</p>
            <p className='fs-7 fw-semibold text-center'>Resistance Levels</p>
            <hr className='col-8 mx-auto'/>
            {pivotDetail.resistance_levels.map((item)=><p className='text-center'>{item.toFixed(6)}</p>)}
        </div>
        <div className='col-6'>
            <p className='fs-7 fw-semibold text-center'>Pivot</p>
            <hr className='col-8 mx-auto'/>
            <p className='text-center'>{pivotDetail.pivot.toFixed(2)}</p>
            <p className='fs-7 fw-semibold text-center'>Support Levels</p>
            <hr className='col-8 mx-auto'/>
            {pivotDetail.support_levels.map((item)=><p className='text-center'>{item.toFixed(6)}</p>)}
        </div>
    </div>
    <div className='border-top'>
        <p className='text-center pt-2'>{pivotDetail.sentiment}</p>

    </div>
</div>
  )
}

export default PivotCard