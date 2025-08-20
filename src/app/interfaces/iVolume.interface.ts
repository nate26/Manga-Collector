import { ICollection } from './iCollection.interface';
import { ISeries } from './iSeries.interface';
import { Shop } from './iShop.interface';
import { IWishlist } from './iWishlist.interface';

export interface ICoverImage {
  name: string;
  url: string;
}

export interface IVolume {
  isbn: string;
  brand: string;
  series: string | null;
  series_id: string;
  display_name: string;
  name: string;
  category: string;
  volume: string;
  url: string;
  record_added_date: string;
  record_updated_date: string;
  release_date: string | null;
  publisher: string | null;
  format: string | null;
  pages: number | null;
  authors: string | null;
  isbn_10: string | null;
  primary_cover_image_url: string;
  other_images: ICoverImage[];
  description: string;
  series_data: ISeries;
  retail_price: number;
  purchase_options: Shop[];
  user_collection_data: ICollection[];
  user_wishlist_data: IWishlist[];
}

export interface Volume {
  id: number;
  isbn: string;
  brand: string;
  display_name: string;
  name: string;
  category: string;
  volume: string;
  url: string;
  release_date: string | null;
  publisher: string | null;
  format: string | null;
  pages: number | null;
  authors: string | null;
  isbn_10: string | null;
  primary_cover_image: string;
  cover_images: ICoverImage[];
  description: string;
  edition: string | null;
  edition_id: string | null;
  series: string | null;
  series_id: string;
  inserted_at: string;
  updated_at: string;
}
