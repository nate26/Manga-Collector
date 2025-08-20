import { IVolume } from './iVolume.interface';

export interface ISeriesVolume {
    isbn: string;
    volume: string;
    category: string;
}

export interface ITheme {
    theme: string;
    votes: number;
}

export interface ISeriesDetails {
    name: string;
    type: string;
}

export interface ISeries {
    series_id: string;
    title?: string;
    associated_titles?: string[];
    url: string;
    category?: string;
    series_match_confidence?: number;
    description?: string;
    cover_image?: string;
    genres?: string[];
    themes?: ITheme[];
    latest_chapter?: number;
    release_status?: string;
    status?: string;
    authors?: ISeriesDetails[];
    publishers?: ISeriesDetails[];
    bayesian_rating?: number;
    rank?: number;
    recommendations?: number[];
    volumes?: ISeriesVolume[];
}

export interface ISeriesRecord extends ISeries {
    volumes: IVolume[];
}