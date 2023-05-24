import axios from 'axios';
import {useEffect, useState} from 'react'

function MovingAvarage({companyName}) {
    const [simpleData, setSimpleData] = useState(null);
    const [expoData, setExpoData] = useState(null);
    const [movingAverage,setMovingAvarage] = useState(5);
    const  fetchData = async () => {
        const simpleDataRequest = axios.get(`http://0.0.0.0:8000/moving-average/simple/${companyName}/2023-01-03/${movingAverage}`)
        const expoDataRequest = axios.get(`http://0.0.0.0:8000/moving-average/expo/${companyName}/2023-01-03/${movingAverage}`)
        const response = await Promise.all([simpleDataRequest,expoDataRequest]);
        setSimpleData(response[0].data);
        setExpoData(response[1].data);
    }
    useEffect(()=>{
        fetchData();
    },[movingAverage])

    if(!simpleData){
        return <div>Yükleniyor</div>
    }
  return (
    <div>
        <div className="col-4 mx-auto">
            <select className="form-select w-100" onChange={(e)=>setMovingAvarage(e.target.value)}>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>
        </div>
        <div className='col-8 border mx-auto mt-3'>
            <div className='col-12 d-flex justify-content-between text-center border-bottom py-2'>
                <div className='col-6 border-end'>
                    <p>Simple {movingAverage}</p>
                </div>
                <div className='col-6'>
                    <p>Expo {movingAverage}</p>
                </div>
            </div>
            <div className='col-12 d-flex justify-content-between py-2'>
                <div className='col-6 border-end d-flex justify-content-around'>
                    <p>{simpleData.ma.toFixed(2)}</p>
                    <p>{simpleData.sentiment}</p>
                </div>
                <div className='col-6 d-flex justify-content-around'>
                    <p>{expoData.ma.toFixed(2)}</p>
                    <p>{expoData.sentiment}</p>
                </div>
            </div>
        </div>
    </div>

  )
}

export default MovingAvarage