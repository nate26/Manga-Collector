import { IManga } from "./iManga.interface";
import { SeriesDB } from "./iSeries.interface";

export interface ICollection {
    id: string;
    user_id: string;
    inserted: string;
    updated: string;
    isbn: string;
    state: string;
    purchaseDate: string;
    cost: number;
    merchant: string;
    giftToMe: boolean;
    read: boolean;
    tags: string[] | string;
}

export interface ICollectionResponse {
    lists: {
        volumes: string[];
        series: string[];
        editions: string[];
    },
    ref: {
        volume_data: { [isbn: string]: IManga };
        series_data: SeriesDB;
    }
}
