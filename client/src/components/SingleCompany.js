import {useEffect, useState} from "react";
import {useParams } from "react-router-dom";

import MovingAvarage from "./MovingAvarage";
import axios from "axios";
import Pivot from "./Pivot";
function SingleCompany() {
  const { name } = useParams();
  const [data,setData] = useState(null)
  const fetchData = async () => {
    const technicalIndicatorData = axios.get(`http://0.0.0.0:8000/technical-indicator/${name}/2023-01-20/?rsi_period=14&stoch_k=14&stoch_d=3&stoch_smooth_k=3&stochrsi_period=14&stochrsi_rsi_period=14&stochrsi_k=3&stochrsi_d=3&macd_fast_period=12&macd_slow_period=26&macd_signal_period=9&adx_period=14&williams_r_period=14&cci_period=14&atr_period=14&hl_period=14&uo_short_period=7&uo_medium_period=14&uo_long_period=28&roc_period=14&bull_bear_power_period=13`);
    const response = await Promise.all([technicalIndicatorData]);
    setData(response[0].data);
  };
  useEffect(() => {
    fetchData();
  }, []);

  console.log(data);
  if(!data){
    return <div>Yükleniyor...</div>
  }
  return (
    <section className="singleCompanySection">
      <div className="container">
        <div className="row">
          <div className="col-12">
            <p className="fw-bold fs-5 text-center">{name}</p>
          </div>
        </div>
        <div className="row technicalIndicator mt-2">
          <div className="col-10 border mx-auto">
            <div className="col-12 adx border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-grid align-items-center">
                <p className="fw-bold fs-6">ADX</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">ADX :</span> {data.technical_values.adx.adx.toFixed(4)}</p>
                <p><span className="fw-semibold">ADX Dmn :</span> {data.technical_values.adx.adx_dmn.toFixed(2)}</p>
                <p><span className="fw-semibold">ADX Dmp :</span> {data.technical_values.adx.adx_dmp.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.adx}</p>
              </div>
            </div> 
            <div className="col-12 atr border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">ATR</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">ATR :</span> {data.technical_values.atr.atr.toFixed(2)}</p>
                <p><span className="fw-semibold">ATR Percentage :</span> {data.technical_values.atr.atr_percentage.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.atr}</p>
              </div>
            </div>
            <div className="col-12 bull-bear-power border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">Bull Bear Power</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">Bear Power :</span> {data.technical_values.bull_bear_power.bear_power.toFixed(2)}</p>
                <p><span className="fw-semibold">Bull Power :</span> {data.technical_values.bull_bear_power.bull_power.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.bull_bear_power}</p>
              </div>
            </div>
            <div className="col-12 cci border-bottom d-flex justify-content-between">
            <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">CCI</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">CCI :</span> {data.technical_values.cci.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.cci}</p>
              </div>
            </div>
            <div className="col-12 hl-ratio border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">HL RATIO</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">HL RATIO :</span> {data.technical_values.hl_ratio.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.hl_ratio}</p>
              </div>
            </div>
            <div className="col-12 macd border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">MACD</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">MACD :</span> {data.technical_values.macd.macd.toFixed(2)}</p>
                <p><span className="fw-semibold">MACD Prev :</span> {data.technical_values.macd.macd_prev.toFixed(2)}</p>
                <p><span className="fw-semibold">MACD S Prev :</span> {data.technical_values.macd.macd_s_prev.toFixed(2)}</p>
                <p><span className="fw-semibold">MACD H :</span> {data.technical_values.macd.macdh.toFixed(2)}</p>
                <p><span className="fw-semibold">MACD S :</span> {data.technical_values.macd.macds.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.macd}</p>
              </div>
            </div>
            <div className="col-12 roc border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">ROC</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">ROC :</span> {data.technical_values.roc.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.roc}</p>
              </div>
            </div>
            <div className="col-12 rsi border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">RSI</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">RSI :</span> {data.technical_values.rsi.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.rsi}</p>
              </div>
            </div>
            <div className="col-12 stoch border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">STOCH</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">STOCH D :</span> {data.technical_values.stoch.stoch_d.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH K :</span> {data.technical_values.stoch.stoch_k.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH Prev D :</span> {data.technical_values.stoch.stoch_prev_d.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH Prev K :</span> {data.technical_values.stoch.stoch_prev_k.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.stoch}</p>
              </div>
            </div>
            <div className="col-12 stochrsi border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">STOCH RSI</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">STOCH Rsi D :</span> {data.technical_values.stoch.stoch_d.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH Rsi K :</span> {data.technical_values.stoch.stoch_k.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH Rsi Prev D :</span> {data.technical_values.stoch.stoch_prev_d.toFixed(2)}</p>
                <p><span className="fw-semibold">STOCH Rsi Prev K :</span> {data.technical_values.stoch.stoch_prev_k.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.stochrsi}</p>
              </div>
            </div>
            <div className="col-12 ultimate-oscillator border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">Ultimate Oscillator</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">Ultimate Oscillator :</span> {data.technical_values.ultimate_oscillator.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.ultimate_oscillator}</p>
              </div>
            </div>
            <div className="col-12 williams-r border-bottom d-flex justify-content-between">
              <div className="col-2 border-end d-flex align-items-center">
                <p className="fw-bold fs-6">Williams R</p>
              </div>
              <div className="col-8 border-end d-flex justify-content-between align-items-center fs-8">
                <p><span className="fw-semibold">Williams R :</span> {data.technical_values.williams_r.toFixed(2)}</p>
              </div>
              <div className="col-2">
                <p>{data.Sentiments.williams_r}</p>
              </div>
            </div>
          </div>
        </div>
        <div className="row mt-5">
          <MovingAvarage companyName={name}/>
        </div>
        <div className="row mt-5">
          <Pivot companyName={name}/>
        </div>
      </div> 
    </section>
  );
}

export default SingleCompany;
