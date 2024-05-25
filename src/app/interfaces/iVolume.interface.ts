import { ICollection } from './iCollection.interface';
import { ISeries } from './iSeries.interface';
import { IShop } from './iShop.interface';
import { IWishlist } from './iWishlist.interface';

export interface ICoverImage {
    name: string;
    url: string;
}

export interface IVolume {
    isbn: string;
    brand: string;
    series: string;
    series_id: string;
    display_name: string;
    name: string;
    category: string;
    volume: string;
    url: string;
    record_added_date: string;
    record_updated_date: string;
    release_date: string;
    publisher: string;
    format: string;
    pages: number;
    authors: string;
    isbn_10: string;
    primary_cover_image_url: string;
    other_images: ICoverImage[];
    description: string;
    series_data: ISeries;
    retail_price: number;
    purchase_options: IShop;
    user_collection_data: ICollection;
    user_wishlist_data: IWishlist;
}
