defmodule MangaServiceWeb.VolumeController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.VolumesDB

  def index(conn, _params) do
    volumes = VolumesDB.list_volumes()

    json(
      conn,
      volumes
      |> Enum.map(fn volume ->
        %{
          id: volume.id,
          name: volume.name,
          format: volume.format,
          description: volume.description,
          category: volume.category,
          url: volume.url,
          isbn: volume.isbn,
          brand: volume.brand,
          series: volume.series,
          series_id: volume.series_id,
          edition: volume.edition,
          edition_id: volume.edition_id,
          display_name: volume.display_name,
          volume: volume.volume,
          release_date: volume.release_date,
          publisher: volume.publisher,
          pages: volume.pages,
          authors: volume.authors,
          isbn_10: volume.isbn_10,
          primary_cover_image: volume.primary_cover_image,
          cover_images: volume.cover_images,
          is_bundle: volume.is_bundle,
          inserted_at: volume.inserted_at,
          updated_at: volume.updated_at
        }
      end)
    )
  end

  def show(conn, %{"id" => isbn}) do
    volume = VolumesDB.get_volume_by_isbn(isbn)

    case volume do
      nil ->
        raise "No record found for ISBN"

      _ ->
        json(conn, %{
          id: volume.id,
          name: volume.name,
          format: volume.format,
          description: volume.description,
          category: volume.category,
          url: volume.url,
          isbn: volume.isbn,
          brand: volume.brand,
          series: volume.series,
          series_id: volume.series_id,
          edition: volume.edition,
          edition_id: volume.edition_id,
          display_name: volume.display_name,
          volume: volume.volume,
          release_date: volume.release_date,
          publisher: volume.publisher,
          pages: volume.pages,
          authors: volume.authors,
          isbn_10: volume.isbn_10,
          primary_cover_image: volume.primary_cover_image,
          cover_images: volume.cover_images,
          is_bundle: volume.is_bundle,
          inserted_at: volume.inserted_at,
          updated_at: volume.updated_at,
          market_data: %{
            retail_price: volume.market_data.retail_price
          },
          series_data: %{
            status: volume.series_data.status,
            category: volume.series_data.category,
            url: volume.series_data.url,
            genres: volume.series_data.genres,
            themes: volume.series_data.themes
          }
        })
    end
  end

  def create(conn, %{"volume" => volume_params}) do
    case VolumesDB.create_volume(volume_params) do
      {:ok, volume} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: volume.id,
          name: volume.name,
          format: volume.format,
          description: volume.description,
          category: volume.category,
          url: volume.url,
          isbn: volume.isbn,
          brand: volume.brand,
          series: volume.series,
          series_id: volume.series_id,
          edition: volume.edition,
          edition_id: volume.edition_id,
          display_name: volume.display_name,
          volume: volume.volume,
          release_date: volume.release_date,
          publisher: volume.publisher,
          pages: volume.pages,
          authors: volume.authors,
          isbn_10: volume.isbn_10,
          primary_cover_image: volume.primary_cover_image,
          cover_images: volume.cover_images,
          is_bundle: volume.is_bundle,
          inserted_at: volume.inserted_at,
          updated_at: volume.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => isbn, "volume" => volume_params}) do
    volume = VolumesDB.get_volume_by_isbn(isbn)

    case VolumesDB.update_volume(volume, volume_params) do
      {:ok, volume} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: volume.id,
          name: volume.name,
          format: volume.format,
          description: volume.description,
          category: volume.category,
          url: volume.url,
          isbn: volume.isbn,
          brand: volume.brand,
          series: volume.series,
          series_id: volume.series_id,
          edition: volume.edition,
          edition_id: volume.edition_id,
          display_name: volume.display_name,
          volume: volume.volume,
          release_date: volume.release_date,
          publisher: volume.publisher,
          pages: volume.pages,
          authors: volume.authors,
          isbn_10: volume.isbn_10,
          primary_cover_image: volume.primary_cover_image,
          cover_images: volume.cover_images,
          is_bundle: volume.is_bundle,
          inserted_at: volume.inserted_at,
          updated_at: volume.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => isbn}) do
    volume = VolumesDB.get_volume_by_isbn(isbn)

    case VolumesDB.delete_volume(volume) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> json(%{success: true})

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete volume"})
    end
  end
end
