import { gql } from 'apollo-angular';

export const GET_ALL_MANGA = gql`
    query List_manga_records {
        list_manga_records {
            manga_records {
                isbn
                record_added_date
                record_updated_date
                name
                format
                volume
                primary_cover_image_url
                other_images {
                    name
                    url
                }
                series
                artist
                author
                description
                genres
                themes
                publisher
                age_rating
                age_rating_bucket
                page_count
                adult
                weight
                url_component
                image_not_final
                retail_price
                release_date
                reprint_date
                pre_book_date
                series_id
                edition_id
            }
            success
            errors
        }
    }
`;
