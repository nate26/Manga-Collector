defmodule MangaService.MarketDBTest do
  use MangaService.DataCase

  alias MangaService.MarketDB

  describe "market" do
    alias MangaService.MarketDB.Market

    import MangaService.MarketDBFixtures

    @invalid_attrs %{isbn: nil, retail_price: nil}

    test "list_market/0 returns all market" do
      market = market_fixture()
      assert MarketDB.list_market() == [market]
    end

    test "get_market!/1 returns the market with given id" do
      market = market_fixture()
      assert MarketDB.get_market!(market.id) == market
    end

    test "create_market/1 with valid data creates a market" do
      valid_attrs = %{isbn: "some isbn", retail_price: 120.5}

      assert {:ok, %Market{} = market} = MarketDB.create_market(valid_attrs)
      assert market.isbn == "some isbn"
      assert market.retail_price == 120.5
    end

    test "create_market/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = MarketDB.create_market(@invalid_attrs)
    end

    test "update_market/2 with valid data updates the market" do
      market = market_fixture()
      update_attrs = %{isbn: "some updated isbn", retail_price: 456.7}

      assert {:ok, %Market{} = market} = MarketDB.update_market(market, update_attrs)
      assert market.isbn == "some updated isbn"
      assert market.retail_price == 456.7
    end

    test "update_market/2 with invalid data returns error changeset" do
      market = market_fixture()
      assert {:error, %Ecto.Changeset{}} = MarketDB.update_market(market, @invalid_attrs)
      assert market == MarketDB.get_market!(market.id)
    end

    test "delete_market/1 deletes the market" do
      market = market_fixture()
      assert {:ok, %Market{}} = MarketDB.delete_market(market)
      assert_raise Ecto.NoResultsError, fn -> MarketDB.get_market!(market.id) end
    end

    test "change_market/1 returns a market changeset" do
      market = market_fixture()
      assert %Ecto.Changeset{} = MarketDB.change_market(market)
    end
  end
end
