import { ISeriesRecord } from './iSeries.interface';
import { IVolume } from './iVolume.interface';

export interface IGQLResponse {
    success: boolean;
    errors: string[];
}

export interface IGQLGetRecord extends IGQLResponse {
    get_record: {
        get_record: IVolume;
    };
}

export interface IGQLAllRecord extends IGQLResponse {
    all_records: {
        all_records: IVolume[];
    };
}

export interface IGQLGetCollectionSeries extends IGQLResponse {
    get_collection_series: {
        get_collection_series: ISeriesRecord[];
    };
}

export interface IGQLGetCollectionVolumes extends IGQLResponse {
    get_collection_volumes: {
        get_collection_volumes: IVolume[];
    };
}