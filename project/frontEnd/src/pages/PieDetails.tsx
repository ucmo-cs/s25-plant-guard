import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchPiHistory } from "../services/piDataApi";
import { PiData } from "../model/PiData";
import LineChart from "../components/charts/LineChart";

export default function PieDetails() {
  const { piId } = useParams();
  const [data, setData] = useState<PiData[]>([]);
  const [loading, setLoading] = useState(true);
  const [range, setRange] = useState<string>("day");

  useEffect(() => {
    const load = async () => {
      if (!piId) {
        console.warn("Missing piId from route params.");
        return;
      }
      try {
        const result = await fetchPiHistory(piId, range);
        setData(result);
      } catch (err) {
        console.error("Error fetching sensor history", err);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [piId, range]);

  if (loading) return <p className="text-white p-6">Loading charts...</p>;

  const labels = data.map((d) =>
    new Date(d.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  );

  const createDataset = (label: string, values: number[]) => ({
    label,
    data: values,
    borderColor: "rgb(192,75,75)",
    backgroundColor: "rgba(0,0,0,0.2)",
    tension: 0.2,
  });

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold text-white">Sensor History — {piId}</h1>

      <div className="flex items-center space-x-4">
        <label htmlFor="range" className="text-white font-medium">Time Range:</label>
        <select
          id="range"
          value={range}
          onChange={(e) => setRange(e.target.value)}
          className="p-2 rounded bg-gray-800 text-white border border-gray-600"
        >
          <option value="hour">Last Hour</option>
          <option value="day">Last Day</option>
          <option value="week">Last Week</option>
          <option value="month">Last Month</option>
          <option value="all">All</option>
        </select>
      </div>

      <div className="flex flex-wrap justify-center gap-6">
        <LineChart title="Temperature" data={{ labels, datasets: [createDataset("Temperature", data.map(d => d.temperature))] }} />
        <LineChart title="Humidity" data={{ labels, datasets: [createDataset("Humidity", data.map(d => d.humidity))] }} />
        <LineChart title="Soil Saturation (RawVal)" data={{ labels, datasets: [createDataset("RawVal", data.map(d => d.rawVal))] }} />
        <LineChart title="Lux" data={{ labels, datasets: [createDataset("Lux", data.map(d => d.lux))] }} />
      </div>
    </div>
  );
}
