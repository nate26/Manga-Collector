defmodule MangaService.SeriesDB.Series do
  use Ecto.Schema
  import Ecto.Changeset

  schema "series" do
    field(:status, :string)
    field(:description, :string)
    field(:title, :string)
    field(:category, :string)
    field(:url, :string)
    field(:series_id, :string)
    field(:associated_titles, {:array, :string})
    field(:series_match_confidence, :decimal)
    field(:volumes, {:array, :string})
    field(:editions, {:array, :string})
    field(:cover_image, :string)
    field(:genres, {:array, :string})
    field(:themes, {:array, :map})
    field(:latest_chapter, :integer)
    field(:release_status, :string)
    field(:authors, {:array, :map})
    field(:publishers, {:array, :map})
    field(:bayesian_rating, :float)
    field(:rank, :integer)
    field(:recommendations, {:array, :string})

    has_many(:volume_details, MangaService.VolumesDB.Volume,
      references: :series_id,
      foreign_key: :series_id
    )

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(series, attrs) do
    series
    |> cast(attrs, [
      :series_id,
      :title,
      :associated_titles,
      :url,
      :category,
      :series_match_confidence,
      :editions,
      :volumes,
      :description,
      :cover_image,
      :genres,
      :themes,
      :latest_chapter,
      :release_status,
      :status,
      :authors,
      :publishers,
      :bayesian_rating,
      :rank,
      :recommendations
    ])
    |> validate_required([
      :series_id,
      :title,
      :associated_titles,
      :url,
      :category,
      :series_match_confidence,
      :editions,
      :volumes,
      :genres,
      :themes,
      :authors,
      :publishers,
      :recommendations
    ])
    |> unique_constraint(:series_id)
  end
end
