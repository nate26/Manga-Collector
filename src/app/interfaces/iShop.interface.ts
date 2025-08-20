export type Shop = {
  item_id: string;
  isbn: string;
  store: string;
  url: string;
  condition: string;
  price: number;
  stock_status: string;
  last_stock_update: string;
  coupon: string;
  is_on_sale: boolean;
  promotion: string;
  promotion_percentage: number;
  backorder_details: string;
  exclusive: boolean;
  is_bundle: boolean;
};

export type ShopVolume = Shop & {
  volume: {
    name: string;
    display_name: string;
    category: string;
    volume: string;
    brand: string;
    series: string;
    series_id: string;
    edition: string;
    edition_id: string;
    release_date: string;
    primary_cover_image: string;
  };
  market: {
    retail_price: number;
  };
};
