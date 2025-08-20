defmodule MangaServiceWeb.VolumesController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.VolumesDB
  alias MangaService.Parsers.MangaData

  def index(conn, _params) do
    volumes =
      VolumesDB.list_volumes_in_series(
        conn.params["series_id"],
        conn.params["limit"],
        conn.params["offset"]
      )

    render(conn, :index, volumes: volumes)
  end

  # def show(conn, %{"isbn" => isbn}) do
  #   volume = VolumesDB.get_volume_by_isbn!(isbn)
  #   render(conn, :show, volume: volume)
  # end

  def get(conn, %{"isbn" => isbn, "user_id" => user_id}) do
    data = MangaData.get_volume_by_isbn_async(isbn, user_id)
    render(conn, :get, data)
  end
end
