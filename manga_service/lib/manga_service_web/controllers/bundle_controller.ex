defmodule MangaServiceWeb.BundleController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.BundlesDB

  def index(conn, _params) do
    bundles = BundlesDB.list_bundles()

    json(
      conn,
      bundles
      |> Enum.map(fn bundle ->
        %{
          id: bundle.id,
          item_id: bundle.item_id,
          series_id: bundle.series_id,
          shop_id: bundle.shop_id,
          primary_cover_image: bundle.primary_cover_image,
          volumes: bundle.volumes,
          volume_start: bundle.volume_start,
          volume_end: bundle.volume_end,
          type: bundle.type,
          inserted_at: bundle.inserted_at,
          updated_at: bundle.updated_at
        }
      end)
    )
  end

  def show(conn, %{"id" => item_id}) do
    bundle = BundlesDB.get_bundle_by_id(item_id)

    case bundle do
      nil ->
        raise "No record found for ID"

      _ ->
        json(conn, %{
          id: bundle.id,
          item_id: bundle.item_id,
          series_id: bundle.series_id,
          shop_id: bundle.shop_id,
          primary_cover_image: bundle.primary_cover_image,
          volumes: bundle.volumes,
          volume_start: bundle.volume_start,
          volume_end: bundle.volume_end,
          type: bundle.type,
          inserted_at: bundle.inserted_at,
          updated_at: bundle.updated_at
        })
    end
  end

  def create(conn, %{"bundle" => bundle_params}) do
    case BundlesDB.create_bundle(bundle_params) do
      {:ok, bundle} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: bundle.id,
          item_id: bundle.item_id,
          series_id: bundle.series_id,
          shop_id: bundle.shop_id,
          primary_cover_image: bundle.primary_cover_image,
          volumes: bundle.volumes,
          volume_start: bundle.volume_start,
          volume_end: bundle.volume_end,
          type: bundle.type,
          inserted_at: bundle.inserted_at,
          updated_at: bundle.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => item_id, "bundle" => bundle_params}) do
    curr_bundle = BundlesDB.get_bundle_by_id(item_id)

    case BundlesDB.update_bundle(curr_bundle, bundle_params) do
      {:ok, bundle} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: bundle.id,
          item_id: bundle.item_id,
          series_id: bundle.series_id,
          shop_id: bundle.shop_id,
          primary_cover_image: bundle.primary_cover_image,
          volumes: bundle.volumes,
          volume_start: bundle.volume_start,
          volume_end: bundle.volume_end,
          type: bundle.type,
          inserted_at: bundle.inserted_at,
          updated_at: bundle.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => item_id}) do
    bundle = BundlesDB.get_bundle_by_id(item_id)

    case BundlesDB.delete_bundle(bundle) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> json(%{success: true})

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete bundle"})
    end
  end
end
