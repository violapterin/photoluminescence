// 1931. Painting a Grid With Three Different Colors [hard]
/*
   You are given two integers `m` and `n`. Consider an `m` by `n`
grid where each cell is initially white. You can paint each cell
red, green, or blue. All cells must be painted.
   Return the number of ways to color the grid with no two adjacent
cells having the same color. Since the answer can be very large,
return it modulo `10^9 + 7`.
   `1 <= m <= 5`
   `1 <= n <= 1000`
*/
// Accepted July 14, 2021.

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
int find_count_coloring(int, int);
bool be_compatible(int, int, int);
bool be_acceptable(int, int);
std::vector<int> convert_digit(int, int);
int modulo(int);
int give_power(int);

int main()
{
   int width = 5;
   int height = 5;
   int count = find_count_coloring(width, height);
   std::cout << "There are " << count << " ways." << std::endl;
   // "580986"
}

int find_count_coloring(int width, int height)
{
   int total = give_power(width);
   std::vector<std::set<int>> many_compatible;
   for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
   {
      std::set<int> set = std::set<int>();
      if (!be_acceptable(width, pattern_new))
      {
         many_compatible.push_back(set);
         continue;
      }
      for (int pattern_old = 0; pattern_old <= total - 1; pattern_old++)
      {
         if (!be_acceptable(width, pattern_old)) { continue; }
         if (!be_compatible(width, pattern_new, pattern_old)) { continue; }
         set.insert(pattern_old);
      }
      many_compatible.push_back(set);
   }

   std::vector<int> record_old(total, 0);
   for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
   {
      if (be_acceptable(width, pattern_new))
      {
         record_old[pattern_new] = 1;
      }
   }

   for (int row = 1; row <= height - 1; row++)
   {
      std::vector<int> record_new(total, 0);
      for (int pattern_new = 0; pattern_new <= total - 1; pattern_new++)
      {
         std::set<int> set = many_compatible[pattern_new];
         for (
            auto pattern_old_ = set.begin();
            pattern_old_ != set.end(); pattern_old_++
         )
         {
            record_new[pattern_new] += record_old[*pattern_old_];
            record_new[pattern_new] = modulo(record_new[pattern_new]);
         }
      }
      record_old = record_new;
   }

   int result = 0;
   for (int pattern = 0; pattern <= total - 1; pattern++)
   {
      result += modulo(record_old[pattern]);
      result = modulo(result);
   }
   result = modulo(result);
   return result;
}

bool be_compatible(int width, int this_pattern, int that_pattern)
{
   std::vector<int> this_many_digit = convert_digit(width, this_pattern);
   std::vector<int> that_many_digit = convert_digit(width, that_pattern);
   for (int head = 0; head <= width - 1; head++)
   {
      if (this_many_digit[head] == that_many_digit[head])
      {
         return false;
      }
   }
   return true;
}

bool be_acceptable(int width, int pattern)
{
   std::vector<int> many_digit = convert_digit(width, pattern);
   int last = many_digit[0];
   for (int head = 1; head <= width - 1; head++)
   {
      int novel = many_digit[head];
      if (last == novel) { return false; }
      last = novel;
   }
   return true;
}

std::vector<int> convert_digit(int width, int pattern)
{
   int remain = pattern;
   std::vector<int> many_digit;
   while (remain)
   {
      int digit = remain % 3;
      many_digit.push_back(digit);
      remain -= digit;
      remain /= 3;
   }
   while (many_digit.size() < width)
   {
      many_digit.push_back(0);
   }
   return many_digit;
}

int modulo(int natural)
{
   int characteristic = 1000000007;
   int result = natural % characteristic;
   return result;
}

int give_power(int power)
{
   int result = 1;
   for (int step = 0; step <= power - 1; step++)
   {
      result *= 3;
   }
   return result;
}
