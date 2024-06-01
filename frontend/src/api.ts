export const BASE: string = "http://127.0.0.1:8000/";

interface Artist {
	name: string;
	img: string;
	id: string;
	content: string;
}

export interface Data {
	genre: string;
	mood: string;
	color: string;
	characteristics: string[];
	artists: Artist[];
	tracks: {
		id: string;
		name: string;
		artist: string;
		duration: string;
	}[];
}

const getBody = (data: any) => {
	return {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	};
};

export const fetchJson = async (url: string, data: any) => {
	const response = await fetch(url, getBody(data));
	return response.json();
};

export const fetchData = async (data: any) => {
	const analysis = await fetchJson(BASE + "analysis", {
		description: data.description,
		key: data.key
	});

	const artists = await fetchJson(BASE + "artist", {
		names: analysis.artists,
	});

	analysis.artists = artists.map((artist: any, index: any) => ({
		...artist,
		content: analysis.content[index],
	}));
	delete analysis.content;

	analysis.tracks = await fetchJson(BASE + "recommendation", {
		ids: analysis.artists.map((artist: any) => artist.id),
	});

	return analysis;
};


// export const fetchDiagnoseData = async (data: any) => {
//     const diagnoseData = await fetchData(data);
//     return diagnoseData;
// };

// // Test
// fetchDiagnoseData({ description: "Korean Soft Indie" })
//     .then((result) => {
//         console.log(result);
//     })
//     .catch((error) => {
//         console.error("Error fetching data:", error);
//     });
//     });
