#ifndef NANDNODE_H
#define NANDNODE_H

#include <AbstractNode.h>


class NANDNode : public AbstractNode
{
    public:
        NANDNode();
        virtual ~NANDNode();
        NANDNode(const NANDNode& other);
        NANDNode& operator=(const NANDNode& other);

    private:
        void Process() override;
};

#endif // NANDNODE_H
