import { Injectable } from '@angular/core';

export type Query = {
    order_by?: string;
    limit?: number;
    offset?: number;
};

@Injectable({
    providedIn: 'root',
})
export class APIQueryService {

    parseQuery<T extends Query>(query: T): string {
        return Object.entries(query).reduce((acc, [key, value]) => {
            if (!value && value !== 0) {
                return acc;
            }
            return acc + key + '=' + value + '&';
        }, (!query.limit ? 'limit=100&' : '') + (!query.offset ? 'offset=0&' : ''));
    }
}
