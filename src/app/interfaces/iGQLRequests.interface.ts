import { ICollection } from './iCollection.interface';
import { ISeriesRecord } from './iSeries.interface';
import { IShopVolume } from './iShopVolume.interface';
import { IVolume } from './iVolume.interface';

export interface IGQLResponse {
  success: boolean;
  errors: string[];
}

export interface IGQLGetRecord extends IGQLResponse {
  get_record: {
    record: IVolume | null;
  };
}

export interface IGQLAllRecord extends IGQLResponse {
  all_records: {
    records: IVolume[];
  };
}

export interface IGQLGetCollectionSeries extends IGQLResponse {
  get_collection_series: {
    records: ISeriesRecord[];
  };
}

export interface IGQLGetCollectionVolumes extends IGQLResponse {
  get_collection_volumes: {
    records: IVolume[];
  };
}

export interface IGQLGetSaleVolumes extends IGQLResponse {
  get_on_sale_volumes: {
    records: IShopVolume[];
  };
}

export interface IGQLSearchVolumes extends IGQLResponse {
  volume_search: {
    records: IVolume[];
  };
}

export interface IGQLModifyCollectionResult {
  modify_collection: {
    __typename: string;
    errors: string[] | null;
    response: ICollection[] | null;
    success: boolean;
  };
}

export interface IGQLDeleteCollectionResult {
  delete_collection_records: {
    __typename: string;
    errors: string[] | null;
    response: string[] | null;
    success: boolean;
  };
}
