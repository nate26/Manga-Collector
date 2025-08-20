defmodule MangaService.BundlesDB.Bundle do
  use Ecto.Schema
  import Ecto.Changeset

  schema "bundles" do
    field(:item_id, :string)
    field(:series_id, :string)
    field(:shop_id, :string)
    field(:primary_cover_image, :string)
    field(:volumes, {:array, :map})
    field(:volume_start, :string)
    field(:volume_end, :string)
    field(:type, :string)

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(bundle, attrs) do
    bundle
    |> cast(attrs, [
      :item_id,
      :series_id,
      :shop_id,
      :primary_cover_image,
      :volumes,
      :volume_start,
      :volume_end,
      :type
    ])
    |> validate_required([:item_id, :series_id, :shop_id, :volumes, :type])
    |> unique_constraint(:item_id)
  end
end
