import { PiData } from "../model/PiData";


export async function getById(pieId: string): Promise<PiData> {
	const all = await getAllLatest();
	const found = all.find(p => p.pieId === pieId);
	if (!found) throw new Error("Pie not found");
	return found;
}


export async function getCurrentPiData(): Promise<PiData[]> {
	const res = await fetch("http://localhost:5264/api/pi/latest");
	if (!res.ok) {
		throw new Error("Failed to fetch from backend");
	}
	return await res.json();
}


export async function fetchPiHistory(piId: string, range: string = "day"): Promise<PiData[]> {
	const res = await fetch(`http://localhost:5264/api/pi/${piId}?range=${range}`);
	if (!res.ok) throw new Error("Failed to fetch sensor history");
	return res.json();
}
