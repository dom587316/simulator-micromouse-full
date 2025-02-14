#include <iostream>
using namespace std;

struct Point {
    int x, y;

    // Constructor
    Point(int _x, int _y) : x(_x), y(_y) {}
};

int main() {
    Point p1(3, 4);  // Khởi tạo điểm (3,4)

    cout << "Point: (" << p1.x << ", " << p1.y << ")" << endl;
    return 0;
}

