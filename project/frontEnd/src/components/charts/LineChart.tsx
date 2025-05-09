import React from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions
} from 'chart.js';
import { Line } from "react-chartjs-2"


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface LineChartProps {
  data: ChartData<'line'>;
  title: string;
}
const backgroundColorPlugin = {
  id: 'custom_canvas_background_color',
  beforeDraw: (chart: any) => {
    const ctx = chart.canvas.getContext('2d');
    ctx.save();
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = '#f0f4f8'; ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  },
};

export default function LineChart({ data, title }: LineChartProps) {
  const options: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: title },
    },

  };
  return (
    <div className="w-[400px] rounded-lg overflow-hidden shadow">
      <Line options={options} data={data} plugins={[backgroundColorPlugin]} />
    </div>
  )
}
