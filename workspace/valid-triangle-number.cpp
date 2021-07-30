// 611. Valid Triangle Number [medium]
/*
   Given an integer array `choice`, return the number of triplets
chosen from the array that can make triangles if we take them
as side lengths of a triangle.
   `1 <= choice.length <= 1000`
   `0 <= choice[i] <= 1000`
*/
// Accepted July 19, 2021.

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
typedef std::vector<int> Choice;
typedef std::map<int, int> Record;
int count_triangle_number(Choice&);
int count_various(Record&, Choice&);
int count_fixed(Record&, int, Choice&);
void push_distinct(Choice&, int);
int pick_two(int);
int pick_three(int);

int main()
{
   Choice choice = {0, 1, 1, 1};
   //Choice choice = {2, 2, 3, 4};
   int count = count_triangle_number(choice);
   std::cout << count << std::endl;
   // "3"
   /* (2,3,4), (2,3,4), (2,2,3) */
}

int count_triangle_number(Choice& choice)
{
   std::sort(choice.begin(), choice.end());
   Choice distinct;
   Record record;
   int key = 0;
   int cumulative = 0;
   for (
      auto value_ = choice.begin();
      value_ != choice.end(); value_++
   )
   {
      if (*value_ == 0) { continue; }
      push_distinct(distinct, *value_);
      while (key < *value_)
      {
         record[key] = cumulative;
         key += 1;
      }
      cumulative += 1;
      record[key] = cumulative;
   }
   if (distinct.empty()) { return 0; }
   while (key < distinct.back() * 2)
   {
      record[key] = cumulative;
      key += 1;
   }
   int number = count_various(record, distinct);
   return number;
}

int count_various(Record& record, Choice& distinct)
{
   if (distinct.empty()) { return 0; }
   int small = distinct[0];
   distinct.erase(distinct.begin());
   int number_fixed = count_fixed(record, small, distinct);
   int number_partial = count_various(record, distinct);
   int number = number_fixed + number_partial;
   return number;
}

int count_fixed(Record& record, int small, Choice& distinct)
{
   int number = 0;
   int novel_small = record[small] - record[small - 1];
   number += pick_three(novel_small);
   if (distinct.empty()) { return number; }
   number += (record[small * 2 - 1] - record[small]) * pick_two(novel_small);
   for (
      auto value_ = distinct.begin();
      value_ != distinct.end(); value_++
   )
   {
      int bound = *value_ + small - 1;
      int novel_medium = record[*value_] - record[*value_ - 1];
      if (novel_medium == 0) { continue; }
      int total_above = record[bound] - record[*value_];
      int add_distinct = total_above * novel_medium;
      int add_pair_medium = novel_medium * (novel_medium - 1) / 2;
      number += novel_small * (add_distinct + add_pair_medium);
   }
   return number;
}

void push_distinct(Choice& choice, int value)
{
   bool whether_update = false;
   if (choice.empty()) { whether_update = true; }
   else if (choice.back() < value) { whether_update = true; }
   if (whether_update) { choice.push_back(value); }
}

int pick_two(int number)
{
   if (number < 2) { return 0; }
   return number * (number - 1) / 2;
}

int pick_three(int number)
{
   if (number < 3) { return 0; }
   return number * (number - 1) * (number - 2) / 6;
}