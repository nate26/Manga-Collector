defmodule MangaService.VolumesDB.Volume do
  use Ecto.Schema
  import Ecto.Changeset
  alias MangaService.{MarketDB.Market, SeriesDB.Series}

  schema "volumes" do
    field(:isbn, :string)
    field(:name, :string)
    field(:display_name, :string)
    field(:category, :string)
    field(:volume, :string)
    field(:url, :string)
    field(:brand, :string)
    field(:series, :string)
    field(:series_id, :string)
    field(:edition, :string)
    field(:edition_id, :string)
    field(:release_date, :date)
    field(:publisher, :string)
    field(:format, :string)
    field(:pages, :integer)
    field(:authors, :string)
    field(:isbn_10, :string)
    field(:description, :string)
    field(:primary_cover_image, :string)
    field(:cover_images, {:array, :map})
    field(:is_bundle, :boolean, default: false)

    belongs_to(:market_data, Market, references: :isbn, foreign_key: :isbn, define_field: false)

    belongs_to(:series_data, Series,
      references: :series_id,
      foreign_key: :series_id,
      define_field: false
    )

    # # TODO fix this?
    # has_many(:shops, MangaServie.ShopsDB.Shop,
    #   references: :isbn,
    #   foreign_key: :isbn
    # )

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(volume, attrs) do
    volume
    |> cast(attrs, [
      :isbn,
      :brand,
      :series,
      :series_id,
      :edition,
      :edition_id,
      :display_name,
      :name,
      :category,
      :volume,
      :url,
      :release_date,
      :publisher,
      :format,
      :pages,
      :authors,
      :isbn_10,
      :primary_cover_image,
      :cover_images,
      :description,
      :is_bundle
    ])
    |> validate_required([:isbn, :display_name, :category, :url, :is_bundle])
    |> unique_constraint(:isbn)
  end
end
