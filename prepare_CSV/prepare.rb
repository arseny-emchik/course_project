require 'csv'

class PrepareCSV
  class << self
    def run
      get_params
      p 'FILE NOT FOUNT!' and return unless File.exist?(Dir.pwd + '/' + @file_name)
      p 'BAD FORMAT! ONLY .CSV' and return unless /.csv$/ =~ @file_name
      overwrite_csv
      create_coded_file
    end

    private

    def get_params
      @file_name = ARGV[0].nil? ? 'no_file' : ARGV[0].to_s
      @new_file_name = ARGV[1].nil? ? "new_#{@file_name}" : ARGV[1].to_s
    end


    def overwrite_csv
      @hash = Hash.new
      @count = 0

      arr = CSV.read(@file_name)
      new_arr = prepare_csv(arr)

      CSV.open(@new_file_name, 'wb') do |csv|
        new_arr.each do |row|
          csv << row
        end
      end
    end

    def prepare_csv(arr_csv)
      new_arr = []
      arr_csv.each do |row|
        new_arr << prepare_row(row)
      end
      new_arr
    end

    def prepare_row(row)
      new_arr_row = []
      row.each do |value|
        new_arr_row << prepare_value(value)
      end
      new_arr_row
    end

    def prepare_value(value)
      (/\-?\d+(\.\d{0,})?/ =~ value) == 0 ? value.to_f : convert_value(value)
    end

    def convert_value(value)
      if @hash[value.to_s].nil?
        @hash[value.to_s] = @count
        new_value = @count
        @count += 1
      else
        new_value = @hash[value.to_s]
      end
      new_value
    end

    def create_coded_file
      CSV.open("coded_#{@file_name}", 'wb') do |csv|
        @hash.each do |key, value|
          csv << [key.to_s, value.to_i]
        end
      end
    end
  end
end

PrepareCSV.run
