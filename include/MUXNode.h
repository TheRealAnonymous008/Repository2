#ifndef MUXNODE_H
#define MUXNODE_H

#include <AbstractNode.h>


class MUXNode : public AbstractNode
{
    public:
        MUXNode();
        MUXNode(int n);
        virtual ~MUXNode();
        MUXNode(const MUXNode& other);
        MUXNode& operator=(const MUXNode& other);

    private:
};

#endif // MUXNODE_H
