import { gql } from 'apollo-angular';

export const GET_MANGA = gql`
    query get_record($isbn: ID!, $user_id: ID) {
        get_record(isbn: $isbn, user_id: $user_id) {
            record {
                isbn
                brand
                series
                display_name
                category
                volume
                url
                user_collection_data {
                    purchaseDate
                }
            }
            success
            errors
        }
    }
`;
