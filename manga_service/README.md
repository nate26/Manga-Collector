# MangaService

To start your Phoenix server:

-   Run `mix setup` to install and setup dependencies
-   Start Phoenix endpoint with `mix phx.server` or inside IEx with `iex -S mix phx.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## Learn more

-   Official website: https://www.phoenixframework.org/
-   Guides: https://hexdocs.pm/phoenix/overview.html
-   Docs: https://hexdocs.pm/phoenix
-   Forum: https://elixirforum.com/c/phoenix-forum
-   Source: https://github.com/phoenixframework/phoenix

DB setup:

mix phx.gen.context Volumes Volume volumes isbn:string brand:string series:string series_id:string edition:string edition_id:string display_name:string name:string category:string volume:string url:string record_added_date:naive_datetime record_updated_date:naive_datetime release_date:date publisher:string format:string pages:integer authors:string isbn_10:string primary_cover_image:string cover_images:array:map description:string

mix phx.gen.context SeriesDB Series series series_id:string title:string associated_titles:array:string url:string category:string series_match_confidence:decimal editions:array:string volumes:array:string description:string cover_image:string genres:array:string themes:array:map latest_chapter:integer release_status:string status:string authors:array:map publishers:array:map bayesian_rating:float rank:integer recommendations:array:string

mix phx.gen.context MarketDB Market market isbn:string retail_price:float

mix phx.gen.context ShopsDB Shop shops store:string condition:string url:string price:float stock_status:string last_stock_update:utc_datetime coupon:string is_on_sale:boolean

mix phx.gen.context UserDB User users id:string username:string email:string password:string collection_id:string picture:string banner:string color:string theme:string personal_stores:array:string

mix phx.gen.context CollectionDB Collection collection id:string user_id:string isbn:string collection:string cost:float store:string purchase_date:date read:boolean tags:array:string rating:float

mix phx.gen.context FollowedDB Followed followed user_id:string follow_type:string follow_id:string
