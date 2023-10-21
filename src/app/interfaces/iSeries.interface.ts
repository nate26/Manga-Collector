import { IManga } from "./iManga.interface";

export interface ISeriesEdition {
    edition: string;
    edition_id: string;
    format: string;
    volumes: {
        isbn: string
        release_date: string
        volume: string
    }[];
}

export interface ISeriesEditionParsed {
    edition: string;
    edition_id: string;
    format: string;
    title: string;
    cover: string;
    volumes: IManga[];
}

export interface ISeries {
    title: string;
    series_id: string
    editions: {[edition_id: string]: ISeriesEdition}
}

export type SeriesDB = {[series_id: string]: ISeries};