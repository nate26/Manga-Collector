export interface Shop {
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
}
