#include <iostream>
#include <queue>  // Thư viện std::queue

using namespace std;

struct Point {
    int x, y;
    Point(int _x, int _y) : x(_x), y(_y) {}
};

int main() {
    queue<Point> q;  // Tạo hàng đợi chứa các điểm Point

    // Đưa 3 điểm vào hàng đợi
    q.push(Point(1, 2));
    q.push(Point(3, 4));
    q.push(Point(5, 6));

    // Lấy và xóa phần tử đầu tiên trong queue (FIFO)
    while (!q.empty()) {
        Point p = q.front();  // Lấy phần tử đầu tiên
        q.pop();              // Xóa phần tử đó

        cout << "Point: (" << p.x << ", " << p.y << ")" << endl;
    }

    return 0;
}

