import { useContext } from 'react'
import FinanceContext from '../context/FinanceContext'
import {Link} from "react-router-dom";
function Table() {
    const {data} = useContext(FinanceContext);
    console.log(data);
  return (
    <section className='table mt-5'>
        <div className='container'>
            <div className='row'>
                <div className='col-12 d-flex flex-wrap gap-3 mx-auto'>
                    {data.map((item,index)=>{return <Link key={index} to={`/${item}`} className='col-2'><button className='w-100'>{item}</button></Link>})}
                </div>
            </div>   
        </div>
    </section>
  )
}

export default Table