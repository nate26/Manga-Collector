import { ICollection } from "./iCollection.interface";

export interface ICoverImage {
    name: string;
    url: string;
}

export interface IManga extends ICollection {
    record_added_date: string;
    last_stock_update: string;
    record_updated_date: string;
    isbn: string;
    display_name: string;
    format: string;
    name: string;
    volume: string;
    cover_images: ICoverImage[];
    primary_cover?: string;
    series: string;
    artist: string;
    author: string;
    description: string;
    genres: string[];
    themes: string[];
    publisher: string;
    age_rating: string;
    age_rating_bucket: string;
    page_count: number;
    adult: boolean;
    weight: number;
    internal_id: number;
    url_component: string;
    is_in_stock: boolean;
    is_purchasable: boolean;
    is_pre_order: boolean;
    is_backorderable: boolean;
    stock_status: string;
    is_on_sale: boolean;
    promos: string[];
    sales: string[];
    publisher_backorder: boolean;
    image_not_final: boolean;
    condition: string;
    exclude_free_shipping: boolean;
    retail_price: number;
    non_member_price: number;
    member_price: number;
    price_lvl_3: number;
    release_date: string;
    reprint_date: string;
    pre_book_date: string;
    series_id: string;
    edition_id: string;
    hovered?: boolean;
}

export interface MangaDB {
    total: number;
    items: {[isbn: string]: IManga};
    last_update: string;
}
